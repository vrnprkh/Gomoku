
SET @user_name = 'username3';

SELECT uid, username
FROM test_database.Users
WHERE username REGEXP @user_name;