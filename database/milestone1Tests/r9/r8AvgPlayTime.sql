--* average play time per game, assumed that it will run after total stats are updated 
SELECT 
    U.uid,
    U.username,
    IFNULL( SEC_TO_TIME(TIME_TO_SEC(US.total_play_time) / US.total_games_played), '00:00:00') AS avg_play_time
FROM Users U
LEFT JOIN UserStats US ON U.uid = US.uid;


