--* total moves for uid 1 -- assumed that it will run after the latest game is added to the Games table
UPDATE UserStats
SET total_moves = total_moves + (
    SELECT IFNULL(COUNT(*), 0)
    FROM DetailedMoves
    JOIN Games ON DetailedMoves.gid = Games.gid
    WHERE Games.uid1 = UserStats.uid
      AND DetailedMoves.move_number % 2 = 1
      AND Games.gid = (
          SELECT MAX(gid)
          FROM Games
          WHERE uid1 = UserStats.uid
      )
)
WHERE uid IN (SELECT uid1 FROM Games);

--* total moves for uid 2 -- assumed that it will run after the latest game is added to the Games table
UPDATE UserStats
SET total_moves = total_moves + (
    SELECT IFNULL(COUNT(*), 0)
    FROM DetailedMoves
    JOIN Games ON DetailedMoves.gid = Games.gid
    WHERE Games.uid2 = UserStats.uid
      AND DetailedMoves.move_number % 2 = 0
      AND Games.gid = (
          SELECT MAX(gid)
          FROM Games
          WHERE uid2 = UserStats.uid
      )
)
WHERE uid IN (SELECT uid2 FROM Games);

--* total play time for uid1 -- assumed that it will run after the latest game is added to the Games table
UPDATE UserStats
SET total_play_time = total_play_time + (
    SELECT IFNULL(SUM(DetailedMoves.move_number * (DetailedMoves.moveTime / 60)), 0)
    FROM DetailedMoves
    JOIN Games ON DetailedMoves.gid = Games.gid
    WHERE Games.uid1 = UserStats.uid
      AND DetailedMoves.move_number % 2 != 0
      AND Games.gid = (
          SELECT MAX(gid)
          FROM Games
          WHERE uid1 = UserStats.uid
      )
)
WHERE uid IN (SELECT uid1 FROM Games);

--* total play time for uid2 -- assumed that it will run after the latest game is added to the Games table 
UPDATE UserStats
SET total_play_time = total_play_time + (
    SELECT IFNULL(SUM(DetailedMoves.move_number * (DetailedMoves.moveTime / 60)), 0)
    FROM DetailedMoves
    JOIN Games ON DetailedMoves.gid = Games.gid
    WHERE Games.uid2 = UserStats.uid
      AND DetailedMoves.move_number % 2 = 0
      AND Games.gid = (
          SELECT MAX(gid)
          FROM Games
          WHERE uid2 = UserStats.uid
      )
)
WHERE uid IN (SELECT uid2 FROM Games);

--* average play time and move number -- assumed that it will run after total stats are updated 
SELECT 
    U.uid,
    U.username,
    IFNULL((US.total_play_time / 60) / US.total_games_played, 0) AS avg_play_time_minutes,
    IFNULL(US.total_moves / US.total_games_played, 0) AS avg_move_number
FROM Users U
LEFT JOIN UserStats US ON U.uid = US.uid;
