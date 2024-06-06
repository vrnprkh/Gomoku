import React from 'react';
import './../App.css';

function About() {
    return (
        <div className="about-container">
            <h1>About Gomoku ⚪⚫</h1>
            <p>
                Gomoku, also known as Five in a Row, is a traditional strategy board game. 
                It is played with two players on a 15x15 board. The players alternate turns 
                placing a stone of their color on an empty cell. The winner is the first player 
                to form an unbroken chain of five stones horizontally, vertically, or diagonally.
            </p>
            <div className="feature-section">
                <h2>Features of Our Gomoku Game:</h2>
                <ul>
                    <li>Play against AI or real players.</li>
                    <li>Choose different themes and board designs.</li>
                    <li>Review your match history and improve your strategy.</li>
                    <li>Competitive ranking system to challenge your skills.</li>
                </ul>
            </div>
            <div className="about-history">
                <h2>The History of Gomoku</h2>
                <p>
                    The game originated in Japan during the Heian period. It has been enjoyed 
                    by millions around the world and remains a favorite in strategy gaming, 
                    teaching essential tactics and forward thinking.
                </p>
            </div>
        </div>
    );
}

export default About;
