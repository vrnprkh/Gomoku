import React, { useState, useEffect } from 'react';
import axios from 'axios';

function SelfLobbies(){
    const [lobbies, setLobbies] = useState([]);

    useEffect(() => {
        fetchLobbies();
    }, []);

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
                            <td>{lobby.uid1}</td>
                            <td>{lobby.uid2}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default SelfLobbies;
