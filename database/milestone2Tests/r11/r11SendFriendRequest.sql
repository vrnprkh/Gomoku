-- Send Friend Request

-- This query adds a new friend request given the to and from uids and a timestamp
-- (*backend checks if opposing friend request exists)
SET @from_user = 1;
SET @to_user = 2;
SET @request_time = "2024-07-09 12:50:17";
INSERT INTO FriendRequests(from_uid, to_uid, requestTime)
VALUES(@from_user, @to_user, @request_time);

