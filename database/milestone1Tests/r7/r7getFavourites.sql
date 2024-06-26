-- get favourites of a user
SET @player1 = 5;
-- Set certain games to favourites
SET @favGID1 = 1009;
SET @favGID2 = 1024;
SET @favGID3 = 1077;

INSERT INTO FavouriteGames (uid, gid)
VALUES (@player1, @favGID1);
INSERT INTO FavouriteGames (uid, gid)
VALUES (@player1, @favGID2);
INSERT INTO FavouriteGames (uid, gid)
VALUES (@player1, @favGID3);


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
JOIN 
    FavouriteGames FG ON G.gid = FG.gid
WHERE 
    FG.uid = @player1
    AND (G.uid1 = @player1 OR G.uid2 = @player1)
    AND G.gid NOT IN (SELECT gid FROM Lobbies);

-- remove same favourites
DELETE FROM FavouriteGames
WHERE uid = @player1 AND gid = @favGID1;
DELETE FROM FavouriteGames
WHERE uid = @player1 AND gid = @favGID2;
DELETE FROM FavouriteGames
WHERE uid = @player1 AND gid = @favGID3;
