CREATE TABLE UserStats (
    uid INT NOT NULL,
    elo INT,
    total_play_time INT,
    total_games_played INT,
    wins INT,
    losses INT,
    draws INT,
    PRIMARY KEY (uid),
    FOREIGN KEY (uid) REFERENCES Users(uid)
);
