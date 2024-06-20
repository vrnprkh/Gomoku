-- R8 Feature:
-- This feature allows users of a Gomoku game application to view and track their performance over time by accessing the user profile’s User Stats page.
-- In particular, this feature displays statistics like average play time per game, win rate and loss rate.

--* average play time per game -- assumed that it will run after total stats are updated 
SELECT 
    U.uid,
    U.username,
    IFNULL((US.total_play_time / 60) / US.total_games_played, 0) AS avg_play_time_minutes
FROM Users U
LEFT JOIN UserStats US ON U.uid = US.uid;

--* win rate -- assumed that it will run after total stats are updated 
UPDATE UserStats
SET win_rate = IF(total_games_played = 0, 0, (wins / total_games_played) * 100)
WHERE uid IN (SELECT uid FROM Users);

--* loss rate -- assumed that it will run after total stats are updated 
UPDATE UserStats
SET loss_rate = IF(total_games_played = 0, 0, (losses / total_games_played) * 100)
WHERE uid IN (SELECT uid FROM Users);
