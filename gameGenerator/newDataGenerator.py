from board import *
import random
import bcrypt
import datetime
import time
import os
# config
NUM_USERS = 1000
FAV_CHANCE = 5 # 1 in X
NUM_GAMES = 10000

# TODO implement this
def encrypt_password(password):
    return bcrypt.hashpw(password, bcrypt.gensalt())

class User:
    def __init__(self, uid : int, username : str, password : str):
        self.uid : int = uid
        self.username : str = username
        self.password : str = password
        self.encrptyed_password : str = str(encrypt_password(password.encode()))[2:-1]
        
        self.gids : list[int] = []
        self.favourites = []

        self.gamesPlayed = 0
        self.playTime = 0
        self.wins = 0
        self.losses = 0
        self.draws = 0
    def addGame(self, gameState : Gomoku, isPlayer1 : bool, gid):
        self.gids.append(gid)
        # add game data given a gamestate
        # Gomoku has information each turn in (x, y, timeSeconds)
        # and player info is passed in
        gamePlayTime = 0 # seconds
        for i in range(len(gameState.moves)):
            gamePlayTime += gameState.moves[i][2]

        self.playTime += gamePlayTime
        if gameState.checkGameState() == None:
            self.draws += 1
        else:
            winner = True if gameState.checkGameState() == PieceState.WHITE else False
            if isPlayer1 == winner:
                self.wins += 1
            else:
                self.losses +=1

    def addFavourites(self, odds : int):
        for gid in self.gids:
            if random.randint(1, odds) == 1:
                self.favourites.append(gid)
        
# create all users
userObjects : list[User] = []
for i in range(NUM_USERS):
    if (i % 50 == 0):
        print(f"GeneratingUser {i} / {NUM_USERS}")
    userObjects.append(User(i, f"{i}_username", f"{i}_password"))


friendRequests = []
EXPECTED_RQ = NUM_USERS
RQ_CHANCE = EXPECTED_RQ/(NUM_USERS * NUM_USERS / 2) 
# send friend requests between users, and automatically create a status for them
for i in range(NUM_USERS):
    for j in range(i + 1, NUM_USERS):
        if random.random() < RQ_CHANCE:
            uid1 = i
            uid2 = j
            base = datetime.datetime.today()
            offset = base - datetime.timedelta(days=random.randint(0, 7), hours=random.randint(0,23), seconds=random.randint(0,3599))
            if random.randint(1,2):
                friendRequests.append((uid1, uid2, str(offset), 0))
            else:
                friendRequests.append((uid2, uid1, str(offset), 0))

friends = []

NORMAL_FRIENDLY_CHANCE = 3
MORE_FRIENDLY_CHANCE = 1

FRIENDLY_CHANCE = 10
# randomly resolve friend requets, and create friends table
for uid in range(NUM_USERS):
    isFriendly = random.randint(1, FRIENDLY_CHANCE) == 1

    newFriends = []
    friendChance = MORE_FRIENDLY_CHANCE if isFriendly else NORMAL_FRIENDLY_CHANCE
    for rq in friendRequests:
        if uid == rq[1] and random.randint(1, friendChance) == 1:
            newFriends.append(rq)
    
    for rq in newFriends:
        friendRequests.remove(rq)
    
    friends.extend([(rq[0], rq[1]) for rq in newFriends])        
    




# create a table of games, and detailed moves, and userstats
games = []
detailedMoves = []

for gid in range(1, NUM_GAMES + 1):
    if gid % 100 == 0:
        print(f"Generating game {gid} / {NUM_GAMES}")
    game = generateRandomGame()
    user1 = userObjects[random.randint(0, len(userObjects) - 1)]
    user2 = userObjects[random.randint(0, len(userObjects) - 1)]
    while user1.uid == user2.uid:
        user2 = userObjects[random.randint(0, len(userObjects) - 1)]

    user1.addGame(game, True, gid)
    user2.addGame(game, False, gid)
    base = datetime.datetime.today()
    offset = base - datetime.timedelta(days=random.randint(0, 7), hours=random.randint(0,23), seconds=random.randint(0,3599))
    games.append([gid, user1.uid, user2.uid, game.draw().replace("\n", ""), 
            {PieceState.BLACK : 0, PieceState.WHITE : 1, None : 2}[game.checkGameState()], offset])

    detailedMoves.extend((
        gid, 
        moveNum, 
        game.moves[moveNum][0], 
        game.moves[moveNum][1], 
        time.strftime(
            "%H:%M:%S",
            time.gmtime(game.moves[moveNum][2])
            )
        ) for moveNum in range(len(game.moves)))


favourites = []
# create favourites
for user in userObjects:
    user.addFavourites(FAV_CHANCE)
    favourites.extend((user.uid, gameid) for gameid in user.favourites)

    






users = [(user.uid, user.username, user.encrptyed_password) for user in userObjects]
userStats = [(
    user.uid, 
    random.randint(1, 2000), # random elo
    time.strftime("%H:%M:%S", time.gmtime(user.playTime)), #seconds to mysql time
    user.wins + user.draws + user.losses,
    user.wins, 
    user.losses, 
    user.draws
    ) for user in userObjects]



def writeData(data, output, outputFolder = "newResults/"):
    outputPath = os.path.join(os.path.dirname(__file__), outputFolder, output)
    with open(outputPath, "w") as f:
        f.write(
            "\n".join([",".join(map(str, e)) for e in data])
        )



# print("\n".join(map(str,users)))
# print("\n".join(map(str,favourites)))
# print("\n".join(map(str, games)))
# print("\n".join(map(str, detailedMoves)))
# print(len(detailedMoves))
# print("\n".join(map(str, friendRequests)))""
# print("\n".join(map(str, friends)))
# print("\n".join(map(str, userStats)))


writeData(users, "users.txt")
writeData(games, "games.txt")
writeData(favourites, "favourites.txt")
writeData(detailedMoves, "detailedMoves.txt")
writeData(friendRequests, "friendRequests.txt")
writeData(friends, "friends.txt")
writeData(userStats, "userStats.txt")