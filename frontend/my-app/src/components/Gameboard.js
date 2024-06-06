import React, { useState } from 'react';
import './../App.css';

function Gameboard() {
  const [board, setBoard] = useState(Array(10).fill().map(() => Array(10).fill(null)));
  const [currentPlayer, setCurrentPlayer] = useState('X');

  const handleCellClick = (row, col) => {
    if (board[row][col] !== null) return; // Prevent changing an already filled cell
    const updatedBoard = board.map((rowArray, rIndex) => 
      rowArray.map((cell, cIndex) => 
        rIndex === row && cIndex === col ? currentPlayer : cell
      )
    );
    setBoard(updatedBoard);
    setCurrentPlayer(currentPlayer === 'X' ? 'O' : 'X'); // Switch player
  };

  return (
    <div className="game-board">
      {board.map((row, rowIndex) => (
        <div key={rowIndex} className="game-row">
          {row.map((cell, colIndex) => (
            <div key={colIndex} className="cell" onClick={() => handleCellClick(rowIndex, colIndex)}>
              {cell}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}

export default Gameboard;
