SET @user_name = 'userNotExist';

SELECT uid, username
FROM test_database.Users
WHERE username REGEXP @user_name;