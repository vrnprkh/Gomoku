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
      const token = localStorage.getItem('token'); 
      console.log("Token:", token);  // Debugging statement

      const response = await axios.get('http://127.0.0.1:5000/api/friend-requests', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      console.log("Friend requests fetched:", response.data);
      setFriendRequests(response.data);
    } catch (error) {
      console.error('Error fetching friend requests:', error);
    }
  };

  const acceptFriendRequest = async (from_uid) => {
    try {
      console.log("Accepting friend request");
      console.log(from_uid)
      const token = localStorage.getItem('token');
      
      await axios.post('http://127.0.0.1:5000/api/accept-request', 
        { from_uid }, 
        {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        }
    );

      
      fetchFriendRequests();
    } catch (error) {
      console.error('Error accepting friend request', error);
    }
  }
  const denyFriendRequest = async (from_uid) => {
    try {
      console.log("Denying friend request");
      console.log(from_uid)
      const token = localStorage.getItem('token');
      
      await axios.post('http://127.0.0.1:5000/api/deny-request', 
        { from_uid }, 
        {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        }
    );
      fetchFriendRequests();
    } catch (error) {
      console.error('Error accepting friend request', error);
    }
  }

  const sendFriendRequest = async (to_uid) => {
    try {
      console.log("Sending friend request")
      const token = localStorage.getItem('token');

      await axios.post('http://127.0.0.1:5000/api/send-request', 
        { to_uid }, 
        {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        }
    );
    } catch (error) {
      console.error('Error sending friend request', error);
    }
  }

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
              <tr key={`${request.from_uid}`}>
                <td>{request.from_uid}</td>
                <td>{request.username}</td>
                <td><button onClick={() => {acceptFriendRequest(request.from_uid)}}>Accept</button>
                <button onClick={() => denyFriendRequest(request.from_uid)}>Deny</button></td>
              </tr>
            ))
          ) : (
            players.map((player) => (
              <tr key={player.uid}>
                <td>{player.uid}</td>
                <td>{player.username}</td>
                <td><button onClick={() => {sendFriendRequest(player.uid)}}>Send Request</button></td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default Players;
