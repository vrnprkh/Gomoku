
SET @user_name = '3_username';

SELECT uid, username
FROM Users
WHERE username REGEXP @user_name;