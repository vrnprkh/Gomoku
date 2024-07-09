SET @user_name = 'userNotExist';

SELECT uid, username
FROM Users
WHERE username REGEXP @user_name;