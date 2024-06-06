import React from 'react';
import './Account.css'; // Assuming you have a separate CSS file for styles

const Account = () => {
    // Static data for demonstration. Replace with dynamic data as needed.
    const playerInfo = {
        username: "PlayerOne",
        rank: "Gold",
        profilePicture: "https://via.placeholder.com/150", // Link to a placeholder image
        matchHistory: [
            { opponent: "PlayerTwo", result: "Win 🏆" },
            { opponent: "PlayerThree", result: "Loss ❌" },
            { opponent: "PlayerFour", result: "Win 🏆" }
        ]
    };

    return (
        <div className="account-container">
            <div className="profile-section">
                <img src={playerInfo.profilePicture} alt="Profile" className="profile-picture" />
                <h1>{playerInfo.username}</h1>
                <p>Rank: {playerInfo.rank}</p>
            </div>
            <div className="history-section">
                <h2>Match History</h2>
                <ul>
                    {playerInfo.matchHistory.map((match, index) => (
                        <li key={index}>{match.opponent} - {match.result}</li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default Account;
