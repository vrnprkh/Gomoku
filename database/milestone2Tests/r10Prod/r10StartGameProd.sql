-- Start Game

-- This query is triggered when a previously unfilled lobby becomes full
-- It updates the Games table with uid2 and closes the lobby
/*
DELIMITER //
CREATE TRIGGER OnLobbyFull
BEFORE UPDATE ON Lobbies
FOR EACH ROW
BEGIN
IF(OLD.open = TRUE AND OLD.uid2 IS NULL AND NEW.uid2 IS NOT NULL) THEN
    -- close lobby
    SET NEW.open = FALSE;
    
    -- update Games table
    UPDATE Games
    SET uid2 = NEW.uid2
    WHERE gid = NEW.gid;
END IF;
END//
DELIMITER ;
*/

-- This query lets a player (@player_id) join a specified open lobby (@game_id)
SET @game_id = 10001;
SET @player_id = 2;
UPDATE Lobbies
SET uid2 = @player_id
WHERE gid = @game_id;

-- Output new Lobbies table
SELECT * FROM Lobbies;

-- -- Revert change
UPDATE Lobbies
SET uid2 = @player_id
WHERE gid = @game_id AND open = TRUE;
