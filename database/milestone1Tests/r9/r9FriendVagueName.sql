SET @player_id = 1;
SET @friend_name = 'name6';
SELECT
    CASE
        WHEN f.uid1 = @player_id THEN f.uid2
        WHEN f.uid2 = @player_id THEN f.uid1
    END AS friend_uid, 
    CASE
        WHEN f.uid1 = @player_id THEN u2.username
        WHEN f.uid2 = @player_id THEN u1.username
    END AS friend_username
    
FROM
    test_database.Friends f
JOIN
    test_database.Users u1 ON f.uid1 = u1.uid
JOIN 
    test_database.Users u2 ON f.uid2 = u2.uid
WHERE 
    (f.uid1 = @player_id AND u2.username REGEXP @friend_name)
    OR (f.uid2 = @player_id AND u1.username REGEXP @friend_name);
