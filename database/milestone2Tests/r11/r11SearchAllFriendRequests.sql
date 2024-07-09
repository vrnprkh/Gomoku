-- Search All Friend Requests

-- This query checks all friend requests a specific user (@player_id) received
SET @player_id = 1;
SELECT *
FROM FriendRequests
WHERE to_uid = @player_id;
