SET @user_name = '4_';

SELECT uid, username
FROM Users
WHERE username REGEXP @user_name;
