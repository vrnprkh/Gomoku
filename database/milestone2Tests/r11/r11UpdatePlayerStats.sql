-- Update Player Stats

-- Create indexes to speed up filtering
-- (we only need to create the indexes once)
/*
CREATE INDEX GameResultsInd ON Games(result);
CREATE INDEX GameUid1ResultsInd ON Games(uid1, result);
CREATE INDEX GameUid2ResultsInd ON Games(uid2, result);
*/


-- Update stats for a specific player (@player_id)
SET @player_id = 0;

WITH PlayerGameData AS ( -- selects all finished games that the specific player has played
    SELECT *
    FROM Games
    WHERE final_game_state IS NOT NULL AND (uid1 = @player_id OR uid2 = @player_id)
)
UPDATE UserStats
SET total_play_time = ( -- sums all moveTime deltas from each move for each game the user plays (will optimize this in the future)
        SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(moveTime)))
        FROM PlayerGameData
        JOIN DetailedMoves USING(gid)
    ),
    total_games_played = (SELECT COUNT(*) FROM PlayerGameData),
    wins = (
		SELECT COUNT(*) FROM PlayerGameData
		WHERE (uid1 = @player_id AND result = 0) OR (uid2 = @player_id AND result = 1)
	),
    losses = (
		SELECT COUNT(*) FROM PlayerGameData
        WHERE (uid1 = @player_id AND result = 1) OR (uid2 = @player_id AND result = 0)
    ),
    draws = (
		SELECT COUNT(*) FROM PlayerGameData
        WHERE result = 2
	)
WHERE uid = @player_id;


-- Updates player elo
UPDATE UserStats
SET elo = wins - losses  -- temp elo calculation: elo = # wins - # losses, will change in the future
WHERE uid = @player_id;


-- Oututs updated player stats
SELECT *
FROM UserStats
WHERE uid = @player_id;

