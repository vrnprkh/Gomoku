import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Account.css';

const Account = () => {
    const [playerInfo, setPlayerInfo] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
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
                // If there's an error, we'll use the default player info
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
  
    return (
      <div className="account-container">
        <div className="profile-section">
          <img src={playerInfo.profilePicture} alt="Profile" className="profile-picture" />
          <h1>{playerInfo.username}</h1>
        </div>
      </div>
    );
};

export default Account;