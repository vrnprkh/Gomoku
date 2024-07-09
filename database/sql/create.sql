CREATE TABLE `Users` (
  `uid` int PRIMARY KEY,
  `username` varchar(16),
  `pwd` varchar(60)
);

CREATE TABLE `UserStats` (
  `uid` int PRIMARY KEY,
  `elo` int,
  `total_play_time` time,
  `total_games_played` int,
  `wins` int,
  `losses` int,
  `draws` int,
  FOREIGN KEY (`uid`) REFERENCES `Users` (`uid`) ON DELETE CASCADE
);

CREATE TABLE `Games` (
  `gid` int PRIMARY KEY,
  `uid1` int,
  `uid2` int,
  `final_game_state` varchar(255),
  `result` int,
  `start_time` timestamp,
  FOREIGN KEY (`uid1`) REFERENCES `Users` (`uid`) ON DELETE SET NULL,
  FOREIGN KEY (`uid2`) REFERENCES `Users` (`uid`) ON DELETE SET NULL
);

CREATE TABLE `FavouriteGames` (
  `uid` int,
  `gid` int,
  PRIMARY KEY (`uid`, `gid`),
  FOREIGN KEY (`gid`) REFERENCES `Games` (`gid`) ON DELETE CASCADE,
  FOREIGN KEY (`uid`) REFERENCES `Users` (`uid`) ON DELETE CASCADE
);

CREATE TABLE `DetailedMoves` (
  `gid` int,
  `move_number` int,
  `coordinateX` int,
  `coordinateY` int,
  `moveTime` time,
  PRIMARY KEY (`gid`, `move_number`),
  FOREIGN KEY (`gid`) REFERENCES `Games` (`gid`) ON DELETE CASCADE
);

CREATE TABLE `Lobbies` (
  `gid` int PRIMARY KEY,
  `uid1` int,
  `uid2` int,
  `open` bool,
  FOREIGN KEY (`gid`) REFERENCES `Games` (`gid`) ON DELETE CASCADE,
  FOREIGN KEY (`uid1`) REFERENCES `Users` (`uid`) ON DELETE CASCADE,
  FOREIGN KEY (`uid2`) REFERENCES `Users` (`uid`) ON DELETE CASCADE
);

CREATE TABLE `Friends` (
  `uid1` int,
  `uid2` int,
  PRIMARY KEY (`uid1`, `uid2`),
  FOREIGN KEY (`uid1`) REFERENCES `Users` (`uid`) ON DELETE CASCADE,
  FOREIGN KEY (`uid2`) REFERENCES `Users` (`uid`) ON DELETE CASCADE
);

CREATE TABLE `FriendRequests` (
  `from_uid` int,
  `to_uid` int,
  `requestTime` timestamp,
  `status` int,
  PRIMARY KEY (`from_uid`, `to_uid`, `requestTime`),
  FOREIGN KEY (`from_uid`) REFERENCES `Users` (`uid`) ON DELETE CASCADE,
  FOREIGN KEY (`to_uid`) REFERENCES `Users` (`uid`) ON DELETE CASCADE
);
