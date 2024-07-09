import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Players() {
  const [players, setPlayers] = useState([]);
  const [friendRequests, setFriendRequests] = useState([]);
  const [search, setSearch] = useState('');
  const [showFriendRequests, setShowFriendRequests] = useState(false);

  useEffect(() => {
    fetchPlayers();
  }, [search]);

  useEffect(() => {
    fetchFriendRequests();
  }, []);

  const fetchPlayers = async () => {
    try {
      console.log("Fetching players with search:", search);
      const response = await axios.get('http://127.0.0.1:5000/api/players', {
        params: { search }
      });
      console.log("Players fetched:", response.data);
      setPlayers(response.data);
    } catch (error) {
      console.error('Error fetching players:', error);
    }
  };

  const fetchFriendRequests = async () => {
    try {
      console.log("Fetching friend requests");
      const response = await axios.get('http://127.0.0.1:5000/api/friend-requests');
      console.log("Friend requests fetched:", response.data);
      setFriendRequests(response.data);
    } catch (error) {
      console.error('Error fetching friend requests:', error);
    }
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Search players"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
      <button onClick={() => setShowFriendRequests(!showFriendRequests)}>
        {showFriendRequests ? 'Show All Players' : 'Show Friend Requests'}
      </button>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Username</th>
          </tr>
        </thead>
        <tbody>
          {showFriendRequests ? (
            friendRequests.map((request) => (
              <tr key={`${request.fromuid}-${request.touid}`}>
                <td>{request.fromuid} -{'>'} {request.touid}</td>
                <td>{request.status}</td>
              </tr>
            ))
          ) : (
            players.map((player) => (
              <tr key={player.uid}>
                <td>{player.uid}</td>
                <td>{player.username}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default Players;
