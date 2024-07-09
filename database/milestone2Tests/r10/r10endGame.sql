-- End Game

-- Update Games and Detailed_Moves tables
SET @game_id = 0;
SET @final_game_state = "";
SET @result = 0;
SET @timestamp = "2024-07-01 11:54:46.060500";
UPDATE Games
SET final_game_state = @final_game_state,
    result = @result,
    timestamp = @timestamp
WHERE gid = @game_id

-- detailed moves---------------- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



-- Update UserStats for a specific player (@player_id) (updates elo, total_play_time, total_games_played)
SET @player_id = 0;

WITH PlayerGameData AS ( -- selects all games that the player has played
    SELECT *
    FROM Games
    WHERE final_game_state IS NOT NULL AND (uid1 = @player_id OR uid2 = @player_id)
)
UPDATE UserStats
SET elo = ( -- temp calculation: elo = # wins - # losses
    SELECT 
    ( -- # wins
        SELECT COUNT(*) FROM PlayerGameData
        WHERE (uid1 = @player_id AND result = 0) OR (uid2 = @player_id AND result = 1)
    ) -
    ( -- # losses
        SELECT COUNT(*) FROM PlayerGameData
        WHERE (uid1 = @player_id AND result = 1) OR (uid2 = @player_id AND result = 0)
    )),
    total_play_time = ( -- sums all moveTime deltas from each move for each game the user plays (will optimize this in the future)
        SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(moveTime)))
        FROM PlayerGameData
        JOIN Detailed_Moves USING(gid)
    ),
    total_games_played = (SELECT COUNT(*) FROM PlayerGameData)
WHERE uid = @player_id;


