-- Start Game

-- This query lets a player (@player_id) join a specified open lobby (@game_id)
SET @game_id = 142;
SET @player_id = 2;
UPDATE Lobbies
SET uid2 = @player_id
WHERE gid = @game_id;

-- This query is triggered when a previously unfilled lobby becomes full
-- It updates the Games table with uid2 and sets the lobby to be closed
CREATE TRIGGER OnLobbyFull
AFTER UPDATE OF uid2 ON Lobbies
REFERENCING OLD ROW o NEW ROW n
FOR EACH ROW
WHEN(o.uid2 IS NULL AND n.uid2 IS NOT NULL)
BEGIN
    UPDATE Lobbies
    SET open = FALSE
    WHERE gid = n.gid

    UPDATE Games
    SET uid2 = n.uid2
    WHERE gid = n.gid
END;

/*
DELIMITER //
CREATE TRIGGER test_database.OnLobbyFull
AFTER UPDATE ON test_database.lobbies
FOR EACH ROW
BEGIN
IF(OLD.uid2 IS NULL AND NEW.uid2 IS NOT NULL) THEN
	-- close lobby
    UPDATE test_database.lobbies
    SET open = FALSE
    WHERE gid = NEW.gid;
    
    -- update Games table
    UPDATE test_database.games
    SET uid2 = NEW.uid2
    WHERE gid = NEW.gid;
END IF;
END//
DELIMITER ;
*/

