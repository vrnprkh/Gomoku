import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';


const Game = () => {
    const { gid } = useParams();
    const [gidState, setGidState] = useState(null);

    useEffect(() => {
        setGidState(gid);
    }, [gid]);

    
    useEffect(() => {
        const fetchTurn = async () => {
            try {
                const token = localStorage.getItem('token'); 
                console.log("Token:", token);  
        
                const response = await axios.get('http://127.0.0.1:5000/api/poll-turn', 
                    {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        },
                        params: { gid }
                    }
                );
    
                console.log(response.data);
    
            } catch (error) {
                console.error('Error polling for turn:', error);
            }
        }

        // Polling interval set to 5 seconds
        const intervalId = setInterval(fetchTurn, 5000);
    
        // Cleanup interval on component unmount
        return () => clearInterval(intervalId);
      }, []);


    return (
        <div>
            <h2>Game</h2>
            {gid != null ? (
                <div>
                    <h4>GID: {gidState}</h4>
                </div>
                ) : (
                    <div>Loading</div>
                )}
        </div>
    );
};

export default Game;
