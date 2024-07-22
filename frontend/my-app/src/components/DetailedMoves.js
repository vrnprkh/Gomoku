import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import './DetailedMoves.css';


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

const DetailedMoves = () => {
    const { gid } = useParams();
    const [gidState, setGidState] = useState(null);
    const [movesInfo, setMovesInfo] = useState([]);
    const [moveIndex, setMoveIndex] = useState(0);
    const [boardState, setBoardState] = useState('.'.repeat(15*15))

    // fetch detailed move info based on gid url param
    useEffect(() => {
        setGidState(gid);
        fetchDetailedMoves();
    }, [gid]);

    // update board state bassed on move index
    useEffect(() => {
        let newBoard = '.'.repeat(15*15);
        
        for (let i = 0; i < moveIndex; i++) {
            let index = movesInfo[i][2] * 15 + movesInfo[i][1];
            newBoard = newBoard.substring(0, index) + (i%2 == 0 ? 'X' : 'O') + newBoard.substring(index+1);
        }
        setBoardState(newBoard)

    }, [moveIndex]);

    // start move index from last move
    useEffect(() => {
        if (movesInfo.length > 0) {
            setMoveIndex(movesInfo.length - 1);
        } else {
            setMoveIndex(0);
        }

    }, [movesInfo]);


    const fetchDetailedMoves = async () => {
        try {
            const token = localStorage.getItem('token'); 
            console.log("Token:", token);
    
            const response = await axios.get('http://127.0.0.1:5000/api/detailed_moves', {
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                params: { gid }
            });
            console.log("Detailed moves fetched:", response.data);
            setMovesInfo(response.data);
        } catch (error) {
            console.error('Error fetching detailed moves:', error);
        }
    };

    return (
        <div className="detailed-move-container">
            <div className="detailed-move-content">
                <h2>Detailed Moves</h2>
                {gid != null && movesInfo.length > 0 ? (
                    <div>
                        <h4>GID: {gidState}</h4>

                        <h3>Move {moveIndex}</h3>

                        <GomokuBoard state={boardState} />
                        
                        <div className="match-btn-container">
                            <button onClick={() => setMoveIndex(Math.max(moveIndex-1, 0))}>Previous Move</button>
                            <button onClick={() => setMoveIndex(Math.min(moveIndex+1, movesInfo.length-1))}>Next Move</button>
                        </div>
                    </div>
                ) : (
                    <div>Loading</div>
                )}
            </div>
        </div>
    );
};

export default DetailedMoves;
