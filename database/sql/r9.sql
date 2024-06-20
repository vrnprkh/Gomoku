--R9 Feature:
--This feature allows users of the Gomoku game application to search for other users or their friends by username. 
--After inputting the search range and username, the feature displays the list of users for further interactions, 
--such as adding friends and request to play with certain users. 



--if checkbox "search for friends only" is selected, the output of the query below will be displayed
--player with uid @player_id can search for their friends with username similar to @friend_name
SELECT
    CASE
        WHEN f.uid1 = @player_id THEN f.uid2
        WHEN f.uid2 = @player_id THEN f.uid1
    END AS friend_uid
FROM
    friends f
JOIN
    Users u1 ON f.uid1 = u1.uid
JOIN 
    Users u2 ON f.uid2 = u2.uid
WHERE 
    (f.uid1 = @player_id AND u2.username REGEXP @friend_name)
    OR (f.uid2 = @player_id AND u1.username REGEXP @friend_name);


--if checkbox "search for friends only" is not selected, the output of the query below will be displayed
--player with uid @player_id can search for other users with username similar to @user_name
SELECT uid
FROM Users
WHERE username REGEXP @user_name;