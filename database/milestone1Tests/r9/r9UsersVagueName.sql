SET @user_name = 'name4';

SELECT uid, username
FROM test_database.Users
WHERE username REGEXP @user_name;
