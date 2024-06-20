-- R6 Feature
-- This query returns the current open game lobbies that a user could join
SELECT l.gid, l.uid1
FROM Lobbies l
WHERE l.open = TRUE;