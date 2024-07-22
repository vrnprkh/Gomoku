import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Lobbies(){
    const [lobbies, setLobbies] = useState([]);
    const [search, setSearch] = useState('');
    const [filteredLobbies, setFilteredLobbies] = useState([]);

    useEffect(() => {
        fetchLobbies();
    }, []);

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
            params: { search }
          });
          console.log("Lobbies fetched:", response.data);
          setLobbies(response.data);
        } catch (error) {
          console.error('Error fetching lobbies:', error);
        }
      };

    const filterLobbies = () =>{
        if (search){
            const filtered = lobbies.filter(lobby =>
                lobby.username.toLowerCase().includes(search.toLowerCase())
            );
            setFilteredLobbies(filtered);                
        } else {
            setFilteredLobbies(lobbies);
        }
        console.log("Filtered lobbies:", filteredLobbies);
    }

    return (
        <div>
            <input
                type="text"
                placeholder="Search for username"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
            />
            <table>
                <thead>
                <tr>
                    <th>Game ID</th>
                    <th>User ID</th>
                    <th>Username</th>
                </tr>
                </thead>
                <tbody>
                {filteredLobbies.map((lobby) => (
                    <tr key={lobby.gid}>
                    <td>{lobby.gid}</td>
                    <td>{lobby.uid1}</td>
                    <td>{lobby.username}</td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    )
}

export default Lobbies;
