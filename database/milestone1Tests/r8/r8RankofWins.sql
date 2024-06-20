SELECT 
    U.uid,
    U.username,
    US.wins,
    RANK() OVER (ORDER BY US.wins DESC) AS rank_of_wins
FROM Users U
LEFT JOIN UserStats US ON U.uid = US.uid;
