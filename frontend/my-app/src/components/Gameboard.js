import React, { useState } from 'react';
import './../App.css';

function Gameboard() {
  const [board, setBoard] = useState(Array(10).fill().map(() => Array(10).fill(null)));
  const [currentPlayer, setCurrentPlayer] = useState('player1');

  const players = {
    player1: 'X',
    player2: 'O'
  };

  const handleCellClick = (row, col) => {
    if (board[row][col] !== null) return;
    const newBoard = board.map((rowArray, rIndex) => 
      rowArray.map((cell, cIndex) => 
        rIndex === row && cIndex === col ? players[currentPlayer] : cell
      )
    );
    setBoard(newBoard);
    setCurrentPlayer(currentPlayer === 'player1' ? 'player2' : 'player1');
  };

  return (
    <div className="game-container">
      <div className="game-board">
        {board.map((row, index) => (
          <div key={index} className="game-row">
            {row.map((cell, cellIndex) => (
              <div key={cellIndex} className="cell" onClick={() => handleCellClick(index, cellIndex)}>
                {cell || ''}
              </div>
            ))}
          </div>
        ))}
      </div>
      <div className="game-info">
        <div className="current-turn">
          Current turn: <span className="player-symbol">{players[currentPlayer]}</span> ({currentPlayer})
        </div>
        <div className="player-list">
          {Object.keys(players).map(player => (
            <div key={player} className={`player ${currentPlayer === player ? 'active' : ''}`}>
              <span className="player-symbol">{players[player]}</span> {player}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Gameboard;
