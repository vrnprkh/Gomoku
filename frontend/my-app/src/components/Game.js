import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

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
    const [boardState, setBoardState] = useState('.'.repeat(15*15))

    const [x, setX] = useState(0);
    const [y, setY] = useState(0);

    
    useEffect(() => {
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
    
            } catch (error) {
                console.error('Error polling for turn:', error);
            }
        }

        // Polling interval set to 5 seconds
        const intervalId = setInterval(fetchTurn, 5000);
    
        // Cleanup interval on component unmount
        return () => clearInterval(intervalId);
    }, []);


    const makeMove = async () => {

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

            console.log("Make move:", response.data);

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
                    <h4>Game Started: {started ? "True" : "False"}</h4>
                    <h4>Turn: {isPlayerTurn ? "Your" : "Opponent's"} turn</h4>

                    <GomokuBoard state={boardState} />

                    

                    <form onSubmit={makeMove}>
                        <div>
                            <label>
                                X:
                                <input type="number" value={x} onChange={(e) => setX(e.target.value)} />
                            </label>
                        </div>
                        <div>
                            <label>
                                Y:
                                <input type="number" value={y} onChange={(e) => setY(e.target.value)} />
                            </label>
                        </div>
                        <button type="submit">Submit</button>
                    </form>


                </div>
                ) : (
                    <div>Loading</div>
                )}
        </div>
    );
};

export default Game;
