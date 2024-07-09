import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import { useNavigate } from 'react-router-dom';
import './Account.css';

const GomokuBoard = ({ state }) => {
    const size = 15;
    const board = state.match(/.{1,15}/g).map((row, rowIndex) => (
        <div className="gomoku-row" key={rowIndex}>
            {row.split('').map((cell, colIndex) => (
                <div
                    className={`gomoku-cell ${cell === '⚪' ? 'white' : cell === '⚫' ? 'black' : ''}`}
                    key={colIndex}
                >
                    {cell === '.' ? '' : cell === 'X' ? '⚪' : '⚫'}
                </div>
            ))}
        </div>
    ));

    return <div className="gomoku-board">{board}</div>;
};

const Account = () => {
    const [playerInfo, setPlayerInfo] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('stats');
    const navigate = useNavigate();

    useEffect(() => {
        const fetchUserData = async () => {
            const token = localStorage.getItem('token');
            const userId = localStorage.getItem('user_id');

            if (!token || !userId) {
                navigate('/login');
                return;
            }

            try {
                const response = await axios.get(`http://127.0.0.1:5000/api/user/${userId}`, {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setPlayerInfo(response.data);
            } catch (error) {
                console.error('Failed to fetch user data:', error);
                if (error.response && error.response.status === 401) {
                    localStorage.removeItem('token');
                    localStorage.removeItem('user_id');
                    navigate('/login');
                }
            } finally {
                setIsLoading(false);
            }
        };

        fetchUserData();
    }, [navigate]);

    if (isLoading) {
        return <div>Loading...</div>;
    }
  
    if (!playerInfo) {
        return <div>Error loading user data</div>;
    }

    const renderStats = () => (
        <div className="stats-section">
            <h2>User Statistics 📊</h2>
            {playerInfo.userStats ? (
                <>
                    <table className="stats-table">
                        <thead>
                            <tr>
                                <th>ELO</th>
                                <th>Total Play Time</th>
                                <th>Total Games</th>
                                <th>Wins</th>
                                <th>Losses</th>
                                <th>Draws</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>{playerInfo.userStats.elo}</td>
                                <td>{playerInfo.userStats.total_play_time}</td>
                                <td>{playerInfo.userStats.total_games_played}</td>
                                <td>{playerInfo.userStats.wins}</td>
                                <td>{playerInfo.userStats.losses}</td>
                                <td>{playerInfo.userStats.draws}</td>
                            </tr>
                        </tbody>
                    </table>
                    <div className="plot-container">
                        <Plot
                            data={[
                                {
                                    x: ['Wins', 'Losses', 'Draws'],
                                    y: [
                                        playerInfo.userStats.wins,
                                        playerInfo.userStats.losses,
                                        playerInfo.userStats.draws
                                    ],
                                    type: 'bar'
                                }
                            ]}
                            layout={{ title: 'Win vs Loss vs Draws', autosize: true }}
                        />
                    </div>
                </>
            ) : (
                <div>No user statistics available</div>
            )}
        </div>
    );

    const renderMatchHistory = () => (
        <div className="match-history-section">
            <h2>Match History 📝</h2>
            {playerInfo.matchHistory && playerInfo.matchHistory.length > 0 ? (
                <div className="match-history-container">
                    {playerInfo.matchHistory.map(match => (
                        <div className="match-history-item" key={match.gid}>
                            <div className="match-info">
                                <div><strong>Game ID:</strong> {match.gid}</div>
                                <div><strong>Player 1:</strong> {match.player1}</div>
                                <div><strong>Player 2:</strong> {match.player2}</div>
                                <div><strong>Result:</strong> {match.result === 0 ? 'Player 1 Wins' : 'Player 2 Wins'}</div>
                            </div>
                            <GomokuBoard state={match.final_game_state} />
                        </div>
                    ))}
                </div>
            ) : (
                <div>No match history available</div>
            )}
        </div>
    );

    const renderFavouriteGames = () => (
        <div className="favourite-games-section">
            <h2>Favourite Games❤️</h2>
            {playerInfo.favouriteGames && playerInfo.favouriteGames.length > 0 ? (
                <div className="match-history-container">
                    {playerInfo.favouriteGames.map(game => (
                        <div className="match-history-item" key={game.gid}>
                            <div className="match-info">
                                <div><strong>Game ID:</strong> {game.gid}</div>
                                <div><strong>Player 1:</strong> {game.player1}</div>
                                <div><strong>Player 2:</strong> {game.player2}</div>
                                <div><strong>Result:</strong> {game.result === 0 ? 'Player 1 Wins' : 'Player 2 Wins'}</div>
                            </div>
                            <GomokuBoard state={game.final_game_state} />
                        </div>
                    ))}
                </div>
            ) : (
                <div>No favourite games available!</div>
            )}
        </div>
    );

    return (
        <div className="account-container">
            <div className="profile-section">
                <img src={playerInfo.profilePicture} alt="Profile" className="profile-picture" />
                <h1>{playerInfo.username}</h1>
            </div>
            <div className="tabs">
                <button onClick={() => setActiveTab('stats')}>Statistics 📊</button>
                <button onClick={() => setActiveTab('history')}>Match History📝</button>
                <button onClick={() => setActiveTab('favourite')}>Favourite Games ❤️</button>
            </div>
            <div className="tab-content">
                {activeTab === 'stats' && renderStats()}
                {activeTab === 'history' && renderMatchHistory()}
                {activeTab === 'favourite' && renderFavouriteGames()}
            </div>
        </div>
    );
};

export default Account;
