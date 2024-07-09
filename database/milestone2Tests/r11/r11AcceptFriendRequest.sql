-- Accept Friend Request

-- These queries accepts an active friend request
-- (*backend checks if friend request exists before making this query)
SET @to_uid = 1;
SET @from_uid = 2;

INSERT INTO Friends(uid1, uid2)
VALUES(@from_user, @to_user);

DELETE FROM FriendRequests
WHERE to_uid = @to_uid AND from_uid = @from_uid;

