--* win rate, assumed that it will run after total stats are updated 
SELECT 
    U.uid,
    U.username,
    IF(US.total_games_played = 0, 0, (US.wins / US.total_games_played) * 100) AS win_rate
FROM Users U
LEFT JOIN UserStats US ON U.uid = US.uid;
