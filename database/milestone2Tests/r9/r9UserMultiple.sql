SET @user_name = 'name';

SELECT uid, username
FROM Users
WHERE username REGEXP @user_name;