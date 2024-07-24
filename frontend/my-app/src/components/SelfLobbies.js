import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function SelfLobbies(){
    const [lobbies, setLobbies] = useState([]);

    useEffect(() => {
        fetchLobbies();
    }, []);
    const nav = useNavigate();
    const fetchLobbies = async () => {
        try {
            const token = localStorage.getItem('token'); 
            console.log("Token:", token);
    
            const response = await axios.get('http://127.0.0.1:5000/api/self-lobbies', {
                headers: {
                    'Authorization': `Bearer ${token}`
                },
            });
            console.log("Lobbies fetched:", response.data);
            setLobbies(response.data);
        } catch (error) {
            console.error('Error fetching lobbies:', error);
        }
    };

    const goToGame = (gid) => {
    
        nav(`../game/${gid}`);
    }

    return (
        <div>
            <table>
                <thead>
                    <tr>
                        <th>Game ID</th>
                        <th>User ID 1</th>
                        <th>User ID 2</th>
                    </tr>
                </thead>
                <tbody>
                    {lobbies.map((lobby) => (
                        <tr key={lobby.gid}>
                            <td>{lobby.gid}</td>
                            <td>{lobby.username1}</td>
                            <td>{lobby.username2}</td>
                            <td><button onClick={() => {goToGame(lobby.gid)}}>Rejoin Game</button></td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default SelfLobbies;
