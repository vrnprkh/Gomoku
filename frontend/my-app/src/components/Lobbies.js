import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Lobbies(){
    const [lobbies, setLobbies] = useState([]);
    const [search, setSearch] = useState('');
    const [filteredLobbies, setFilteredLobbies] = useState([]);
    const [showFriendsOnly, setShowFriendsOnly] = useState(false);

    useEffect(() => {
        fetchLobbies();
    }, [search, showFriendsOnly]);

    useEffect(() => {
        filterLobbies();
    }, [search, lobbies]);

    const fetchLobbies = async () => {
        try {
            const token = localStorage.getItem('token'); 
            console.log("Token:", token);
    
            const response = await axios.get('http://127.0.0.1:5000/api/lobbies', {
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                params: { search, show_friends_only: showFriendsOnly }
            });
            console.log("Lobbies fetched:", response.data);
            setLobbies(response.data);
        } catch (error) {
            console.error('Error fetching lobbies:', error);
        }
    };

    const joinLobby = async (gid) => {
        try {
            const token = localStorage.getItem('token'); 
            console.log("Token:", token);  
    
            const response = await axios.post('http://127.0.0.1:5000/api/join_lobby', 
                { gid },
                {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                }
            );
            console.log("Join lobby response:", response.data);
            fetchLobbies(); // Refresh lobbies after joining
        } catch (error) {
            console.error('Error joining lobby:', error);
        }
    };

    const createLobby = async () => {
        try {
            const token = localStorage.getItem('token'); 
            console.log("Token:", token);  
    
            const response = await axios.post('http://127.0.0.1:5000/api/create_lobby', 
                { },
                {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                }
            );

            console.log("Create lobby response:", response.data);
            fetchLobbies(); // Refresh lobbies after creating lobby
        } catch (error) {
            console.error('Error creating lobby:', error);
        }
    }

    const filterLobbies = () => {
        if (search) {
            const filtered = lobbies.filter(lobby =>
                lobby.username.toLowerCase().includes(search.toLowerCase())
            );
            setFilteredLobbies(filtered);                
        } else {
            setFilteredLobbies(lobbies);
        }
        console.log("Filtered lobbies:", filteredLobbies);
    };

    return (
        <div>
            <input
                type="text"
                placeholder="Search for open Lobbies"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
            />
            <button onClick={() => setShowFriendsOnly(!showFriendsOnly)}>
                {showFriendsOnly ? 'Show All Lobbies' : 'Show Friends Lobbies'}
            </button>

            <button onClick={() => createLobby()}>Create Lobby</button>

            <table>
                <thead>
                    <tr>
                        <th>Game ID</th>
                        <th>User ID</th>
                        <th>Username</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {filteredLobbies.map((lobby) => (
                        <tr key={lobby.gid}>
                            <td>{lobby.gid}</td>
                            <td>{lobby.uid1}</td>
                            <td>{lobby.username}</td>
                            <td>
                                <button onClick={() => joinLobby(lobby.gid)}>Join</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}

export default Lobbies;
