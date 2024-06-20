-- If we search for only lobbies created by the friend of a particular user with uid: @player_id, we run the following query:
SELECT l.gid, l.uid1
FROM Lobbies l
JOIN (
    SELECT
        CASE
            WHEN f.uid1 = 9 THEN f.uid2
            WHEN f.uid2 = 9 THEN f.uid1
        END AS friend_uid
    FROM Friends f
) f
ON f.friend_uid = l.uid1
WHERE l.open=TRUE;