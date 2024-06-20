SET @user_name = 'name4';

SELECT uid, username
FROM Users
WHERE username REGEXP @user_name;
