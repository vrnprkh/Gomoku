-- Note that this is intended to be not part of the Milestone 1 feature.

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

--* total play time for uid1 and uid2 -- assumed that it will run after the latest game is added to the Games table
UPDATE UserStats
SET total_play_time = total_play_time + (
    SELECT IFNULL(SUM(DetailedMoves.moveTime / 60), 0) AS latest_game_time
    FROM DetailedMoves
    JOIN Games ON DetailedMoves.gid = Games.gid
    WHERE Games.gid = (
        SELECT MAX(gid)
        FROM Games
        WHERE Games.uid1 = UserStats.uid OR Games.uid2 = UserStats.uid
    )
    AND (Games.uid1 = UserStats.uid OR Games.uid2 = UserStats.uid)
)
WHERE uid IN (
    SELECT uid1 FROM Games WHERE gid = (SELECT MAX(gid) FROM Games WHERE uid1 = UserStats.uid)
) OR uid IN (
    SELECT uid2 FROM Games WHERE gid = (SELECT MAX(gid) FROM Games WHERE uid2 = UserStats.uid)
);

--* average move per game -- assumed that it will run after total stats are updated 
SELECT 
    U.uid,
    U.username,
    IFNULL(US.total_moves / US.total_games_played, 0) AS avg_move_number
FROM Users U
LEFT JOIN UserStats US ON U.uid = US.uid;
