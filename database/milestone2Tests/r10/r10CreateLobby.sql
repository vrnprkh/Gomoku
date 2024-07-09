-- Create Lobby

-- This query creates a new game with a given generated gid (@game_id) and uid (@player_id, who created the game)
SET @game_id = 232;
SET @player_id = 1;
INSERT INTO Games(gid, uid1, uid2, final_game_state, result, start_time)
VALUES(@game_id, @player_id, NULL, NULL, NULL, NULL);

-- A new associated open lobby is created automatically for each open game
CREATE TRIGGER OnNewGame
AFTER INSERT ON Games
REFERENCING NEW ROW n
FOR EACH ROW
    INSERT INTO Lobbies(gid, uid1, uid2, open) VALUES(n.gid, n.uid1, NULL, FALSE);

/*
CREATE TRIGGER test_database.OnNewGame
AFTER INSERT ON test_database.games
FOR EACH ROW
    INSERT INTO test_database.lobbies(gid, uid1, uid2, open) VALUES(NEW.gid, NEW.uid1, NULL, FALSE);
*/
