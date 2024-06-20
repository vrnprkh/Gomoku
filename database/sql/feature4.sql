SELECT
    CASE
        WHEN f.uid1 = @player_id THEN f.uid2
        WHEN f.uid2 = @player_id THEN f.uid1
    END AS friend_uid
FROM
    friends f
JOIN
    user u1 ON f.uid1 = u1.uid
JOIN 
    user u2 ON f.uid2 = u2.uid
WHERE 
    (f.uid1 = @player_id AND u2.username REGEXP @friend_name)
    OR (f.uid2 = @player_id AND u1.username REGEXP @friend_name);


SELECT uid
FROM User
WHERE username REGEXP @user_name;