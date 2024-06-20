
SET @user_name = 'username3';

SELECT uid, username
FROM Users
WHERE username REGEXP @user_name;