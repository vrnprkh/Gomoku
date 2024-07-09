-- R6 Feature
-- This query returns the open lobbies created by their friends for a given user (@player_id)
SET @player_id = 4;
SELECT l.gid, l.uid1
FROM Lobbies l
JOIN (
    SELECT DISTINCT
        CASE
            WHEN f.uid1 = @player_id THEN f.uid2
            WHEN f.uid2 = @player_id THEN f.uid1
        END AS friend_uid
    FROM Friends f
) f
ON f.friend_uid = l.uid1
WHERE l.open=TRUE;