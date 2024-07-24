import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import './../App.css';

const GomokuBoard = ({ state }) => {
    const size = 15;
    const board = state.match(/.{1,15}/g).map((row, rowIndex) => (
        <div className="gomoku-row" key={rowIndex}>
            {row.split('').map((cell, colIndex) => (
                <div
                    className={`gomoku-cell ${cell === '⚫' ? 'white' : cell === '⚪' ? 'black' : ''}`}
                    key={colIndex}
                >
                    {cell === '.' ? '' : cell === 'X' ? '⚫' : '⚪'}
                </div>
            ))}
        </div>
    ));

    return <div className="gomoku-board">{board}</div>;
};

const Game = () => {
    const { gid } = useParams();
    const [started, setStarted] = useState(false);
    const [isPlayerTurn, setIsPlayerTurn] = useState(false);
    const [board, setBoard] = useState(Array(15).fill().map(() => Array(15).fill(null)));
    const [gameOver, setGameOver] = useState(false);
    const [players, setPlayers] = useState([null, null]);
    const [turn, setTurn] = useState(0);

    const pSymbol = ['⚪', '⚫'];

    const fetchTurn = async () => {
        try {
            const token = localStorage.getItem('token'); 
            console.log("Token:", token);  
    
            const response = await axios.get('http://127.0.0.1:5000/api/poll-turn', 
                {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                    params: { gid }
                }
            );

            console.log(response.data);

            setStarted(response.data["started"]);
            setIsPlayerTurn(response.data["turn"]);
            setGameOver(response.data["gameOver"]);
            setPlayers([response.data["username1"], response.data["username2"]]);
            
            // draw updated board
            let newBoard = Array(15).fill().map(() => Array(15).fill(null));
            let moves = response.data["moves"];
            setTurn(moves.length%2);
            for (let i = 0; i < moves.length; i++) {
                let x = moves[i]["coordinateX"];
                let y = moves[i]["coordinateY"];
                newBoard[y][x] = (i%2 == 0) ? pSymbol[0] : pSymbol[1];
            }
            setBoard(newBoard);

        } catch (error) {
            console.error('Error polling for turn:', error);
        }
    }

    useEffect(() => {
        fetchTurn();
    }, []);
    
    useEffect(() => {
        fetchTurn();

        // Polling interval set to 5 seconds
        const intervalId = setInterval(fetchTurn, 1000);
    
        // Cleanup interval on component unmount
        return () => clearInterval(intervalId);
    }, []);

    const makeMove = async (x, y) => {
        try {
            const token = localStorage.getItem('token'); 
            console.log("Token:", token);  
    
            const response = await axios.post('http://127.0.0.1:5000/api/make-move', 
                { gid, x, y },
                {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                }
            );

            fetchTurn();

        } catch (error) {
            console.error('Error making move:', error);
        }
    }

    return (
        <div>
            <h2>Game</h2>
            {gid != null ? (
                <div>
                    <h4>GID: {gid}</h4>
                    

                    <div className="game-container">
                        <div className="game-board">
                            {board.map((row, index) => (
                            <div key={index} className="game-row">
                                {row.map((cell, cellIndex) => (
                                <div key={cellIndex} className="cell" onClick={() => makeMove(cellIndex, index)}>
                                    {cell || ''}
                                </div>
                                ))}
                            </div>
                            ))}
                        </div>
                        <div className="game-info">
                            <div className="current-turn">
                                {started ? (
                                    <div>Turn: <span className="player-symbol">{pSymbol[turn]}</span> {players[turn]} ({isPlayerTurn ? "You" : "Opponent"})</div>
                                ) : (
                                    <div>Waiting for players...</div>
                                )}
                            </div>
                            <div className="player-list">
                                <div><span className="player-symbol">{pSymbol[0]}</span>{players[0]}</div>
                                <div><span className="player-symbol">{pSymbol[1]}</span>{players[1]}</div>
                            </div>
                        </div>
                    </div>

                    { !gameOver || (
                        <center>
                            <h2>Game Over!</h2>
                        </center>
                    ) }
                </div>
                ) : (
                    <div>
                        <p>Loading...</p>
                    </div>
                )}
        </div>
    );
};

export default Game;
