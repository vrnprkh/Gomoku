import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Friends() {
  const [friends, setFriends] = useState([]);
  const [search, setSearch] = useState('');
  const [filteredFriends, setFilteredFriends] = useState([]);

  useEffect(() => {
    fetchFriends();
  }, []);

  useEffect(() => {
    filterFriends();
  }, [search, friends]);

  const fetchFriends = async () => {
    try {
      console.log("Fetching friends");

      const token = localStorage.getItem('token'); 
      console.log("Token:", token);  // Debugging statement

      const response = await axios.get('http://127.0.0.1:5000/api/friends', {
        headers: {
          'Authorization': `Bearer ${token}`
        },
        params: { search }
      });
      console.log("Friends fetched:", response.data);
      setFriends(response.data);
    } catch (error) {
      console.error('Error fetching friends:', error);
    }
  };

  const filterFriends = () => {
    if (search) {
      const filtered = friends.filter(friend =>
        friend.friend_username.toLowerCase().includes(search.toLowerCase())
      );
      setFilteredFriends(filtered);
    } else {
      setFilteredFriends(friends);
    }
    console.log("Filtered friends:", filteredFriends);  // Debugging statement
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Search friends"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Username</th>
          </tr>
        </thead>
        <tbody>
          {filteredFriends.map((friend) => (
            <tr key={friend.friend_uid}>
              <td>{friend.friend_uid}</td>
              <td>{friend.friend_username}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Friends;
