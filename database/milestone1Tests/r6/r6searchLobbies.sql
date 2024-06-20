-- R6 Feature:
-- This query returns the current open game lobbies that a user could join. Users can optionally only look for lobbies created by their friends to join.

-- If we search for all open lobbies, we run the following sample query
SELECT *
FROM Lobbies l
WHERE l.open = TRUE;

-- If we search for only lobbies created by the friend of a particular user with uid: @player_id, we run the following query:
SELECT *
FROM Lobbies l
WHERE l.open = True
JOIN (
    SELECT DISTINCT
        CASE
            WHEN f.uid1 = 1 THEN f.uid2
            WHEN f.uid2 = 1 THEN f.uid1
        END AS friend_uid
    FROM Friends f
) f
ON f.friend_uid = l.uid1;
