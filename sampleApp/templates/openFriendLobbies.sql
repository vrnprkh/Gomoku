SELECT l.gid, l.uid1
FROM Lobbies l
JOIN (
    SELECT DISTINCT
        CASE
            WHEN f.uid1 = {player} THEN f.uid2
            WHEN f.uid2 = {player} THEN f.uid1
        END AS friend_uid
    FROM Friends f
) f
ON f.friend_uid = l.uid1
WHERE l.open=TRUE;