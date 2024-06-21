-- get favourites of same user (empty)
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
JOIN 
    FavouriteGames FG ON G.gid = FG.gid
WHERE 
    FG.uid = @player1
    AND (G.uid1 = @player1 OR G.uid2 = @player1)
    AND G.gid NOT IN (SELECT gid FROM Lobbies);
