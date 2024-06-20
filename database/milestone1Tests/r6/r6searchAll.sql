-- R6 Feature:
-- This query returns the current open game lobbies that a user could join. Users can optionally only look for lobbies created by their friends to join.

-- If we search for all open lobbies, we run the following sample query
SELECT l.gid, l.uid1
FROM Lobbies l
WHERE l.open = TRUE;