from board import *
import os
import time

# to use, run this script, and change the createMany paramaters at the bottom
# the first paramters is the number of users you want to generate for,
# and the second is just the number of games each user will play with each other user
# for example, for createMany(5, 2)
# for each possible pairing of the 5 users we will simulate 2 games
# this will give us a total of 20 games


def createMany(numUsers, numGames):
    uids = [i for i in range(numUsers)]
    gid = 100 # change this to zero if you want to start at 0
    gameData = []
    for i in range(numUsers):
        for j in range(i + 1, numUsers):
            for _ in range(numGames):
                gameData.append(createGameData(uids[i], uids[j], gid))
                gid += 1
    
    gDataString = ""
    for e in gameData:
        gDataString += ', '.join(map(str,e)) + "\n"

    # fixing relative path issues
    dirname = os.path.dirname(__file__)
    f1name = os.path.join(dirname, "results/gameData.txt")
    with open(f1name, "w") as f:
        f.write(gDataString)
    f2name = os.path.join(dirname, "results/userData.txt")
    with open(f2name, "w") as f:
        f.write(
            "\n".join(', '.join(map(str, [uid, f"username{uid}", f"password{uid}"])) for uid in uids) + "\n"
        )


    pass


def createGameData(uid1, uid2, gid):
    gameState = generateRandomGame()
    # uid1 is black
    # uid2 is white
    return [gid, uid1, uid2, gameState.draw().replace("\n", ""), 
            {PieceState.BLACK : "BLACK", PieceState.WHITE : "WHITE", None : "DRAW"}[gameState.checkGameState()]]

startTime = time.time()
createMany(10, 5)