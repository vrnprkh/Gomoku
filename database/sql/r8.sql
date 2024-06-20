-- R8 Feature:
-- This feature allows users of a Gomoku game application to view and track their performance over time by accessing the user profile’s User Stats page.
-- In particular, this feature displays statistics like average play time per game, win rate and loss rate.

--* average play time per game -- assumed that it will run after total stats are updated 
SELECT 
    U.uid,
    U.username,
    IFNULL(
        TIME_TO_SEC(US.total_play_time) / 60 / US.total_games_played, 
        0
    ) AS avg_play_time_minutes
FROM Users U
LEFT JOIN UserStats US ON U.uid = US.uid;

--* win rate -- assumed that it will run after total stats are updated 
SELECT 
    U.uid,
    U.username,
    IF(US.total_games_played = 0, 0, (US.wins / US.total_games_played) * 100) AS win_rate
FROM Users U
LEFT JOIN UserStats US ON U.uid = US.uid;

--* loss rate -- assumed that it will run after total stats are updated 
SELECT 
    U.uid,
    U.username,
    IF(US.total_games_played = 0, 0, (US.losses / US.total_games_played) * 100) AS loss_rate
FROM Users U
LEFT JOIN UserStats US ON U.uid = US.uid;
