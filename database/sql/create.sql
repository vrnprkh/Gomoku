CREATE TABLE Users(
    uid INT NOT NULL,
    username varchar,
    password varchar,
    PRIMARY KEY (uid)
);

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

CREATE TABLE Friends (
    uid1 INT NOT NULL,
    uid2 INT NOT NULL,
    PRIMARY KEY(uid1, uid2),
    FOREIGN KEY (uid1) REFERENCES Users(uid),
    FOREIGN KEY (uid2) REFERENCES Users(uid)
);
CREATE TABLE Games (
    gid INT NOT NULL,
    uid1 INT,
    uid2 INT,
    final_game_state varchar,
    result int, -- TODO check this later
    PRIMARY KEY (gid),
    FOREIGN KEY (uid1) REFERENCES Users(uid),
    FOREIGN KEY (uid2) REFERENCES Users(uid),
);

CREATE TABLE Lobbies (
    gid INT NOT NULL,
    uid1 INT,
    uid2 INT,
    isOpen INT, -- TODO change this in diagrams since bool can't exist
    PRIMARY KEY (gid),
    FOREIGN KEY (gid), REFERENCES Games(gid),
    FOREIGN KEY (uid1) REFERENCES Users(uid),
    FOREIGN KEY (uid2) REFERENCES Users(uid)  
);
