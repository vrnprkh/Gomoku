-- Create Lobby

-- A new associated open lobby is created automatically for each open game
-- (we only need to create the trigger once)
/*
CREATE TRIGGER OnNewGame
AFTER INSERT ON Games
FOR EACH ROW
    INSERT INTO Lobbies(gid, uid1, uid2, open) VALUES(NEW.gid, NEW.uid1, NULL, TRUE);
*/


-- This query creates a new game with a given generated gid (@game_id) and uid (@player_id, who created the game)
SET @game_id = 90003;
SET @player_id = 3;
INSERT INTO Games(gid, uid1, uid2, final_game_state, result, start_time)
VALUES(@game_id, @player_id, NULL, NULL, NULL, NULL);

-- Output new Games and Lobbies table
SELECT * FROM Games
ORDER BY gid DESC
LIMIT 10;

SELECT * FROM Lobbies;

-- Revert change
DELETE FROM Games
WHERE gid = @game_id;
