-- Create indexes to speed up filtering
-- (we only need to create the indexes once)
/*
CREATE INDEX GameUid1Ind ON Games(uid1);
CREATE INDEX GameUid2Ind ON Games(uid2);
*/


-- get all games for a specific player (@player1)
SET @player1 = 5;

SELECT 
    G.final_game_state,
    U1.username AS player1,
    U2.username AS player2,
    G.result
FROM 
    Games G
JOIN 
    Users U1 ON G.uid1 = U1.uid
JOIN 
    Users U2 ON G.uid2 = U2.uid
WHERE 
    (G.uid1 = @player1 OR G.uid2 = @player1)
    AND G.gid NOT IN (SELECT gid FROM Lobbies);
