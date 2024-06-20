from board import *
import os
import time
import random
# to use, run this script, and change the createMany paramaters at the bottom
# the first paramters is the number of users you want to generate for,
# and the second is just the number of games each user will play with each other user
# for example, for createMany(5, 2)
# for each possible pairing of the 5 users we will simulate 2 games
# this will give us a total of 20 games


def createMany(numUsers, numGames):
    uids = [i for i in range(numUsers)]
    gid = 1000 # change this to zero if you want to start at 0
    gameData = []
    for i in range(numUsers):
        for j in range(i + 1, numUsers):
            for _ in range(numGames):
                gameData.append(createGameData(uids[i], uids[j], gid))
                gid += 1
    
    gDataString = ""
    for e in gameData:
        gDataString += ', '.join(map(str,e)) + "\n"

    # get all pairs of users that are not the same, and randomly decide if two are friends
    friendChance = 5 # 1 / (friendChance)
    friends = [(uids[i], uids[j]) for i in range(numUsers) for j in range(i + 1, numUsers) if random.randint(0, friendChance - 1) == 0]

    # create userStat table for each user
    userStats = createUserStats(gameData, uids)


    # fixing relative path issues
    dirname = os.path.dirname(__file__)
    f1name = os.path.join(dirname, "results/gameData.txt")
    with open(f1name, "w") as f:
        f.write("gid, uid1, uid2, final_game_state, result\n"+gDataString)
    f2name = os.path.join(dirname, "results/userData.txt")
    with open(f2name, "w") as f:
        f.write(
            "uid, username, password\n"
            +
            "\n".join(', '.join(map(str, [uid, f"username{uid}", f"password{uid}"])) for uid in uids) + "\n"
        )
    f3name = os.path.join(dirname, "results/friends.txt")
    with open(f3name, "w") as f:
        f.write("uid1, uid2\n"
            + "\n".join([f"{pair[0]}, {pair[1]}" for pair in friends]))
    

    
    f4name = os.path.join(dirname, "results/userStats.txt")    
    with open(f4name, "w") as f:
        f.write(
            "uid, elo, total_play_time, total_games_played, wins, losses, draws\n"
            +
            "\n".join([", ".join(map(str, userStats[uid])) for uid in uids])
        )
        

    


def createGameData(uid1, uid2, gid):
    gameState = generateRandomGame()
    # uid1 is black
    # uid2 is white
    return [gid, uid1, uid2, gameState.draw().replace("\n", ""), 
            {PieceState.BLACK : "BLACK", PieceState.WHITE : "WHITE", None : "DRAW"}[gameState.checkGameState()]]


# clean this up later this code is terrible
def createUserStats(gameData, uids):
    stats = dict()
    for uid in uids:
        # uid[0], elo[1], total_play_time[2], total_games_played[3], wins[4], losses[5], draws[6]
        stats[uid] = [uid, random.randint(1,1000), 0, 0, 0, 0, 0]
    for game in gameData:
        
        uid1 = game[1]
        uid2 = game[2]
        # random time of 300-600 seconds (5-10 min)
        timeplayed = random.randint(300,600)
        stats[uid1][2] += timeplayed
        stats[uid2][2] += timeplayed

        stats[uid1][3] += 1
        stats[uid2][3] += 1

        if game[4] == "WHITE":
            stats[uid1][4] += 1
            stats[uid2][5] += 1
        elif game[4] == "BLACK":
            stats[uid1][5] += 1
            stats[uid2][4] += 1
        else:
            stats[uid1][6] += 1
            stats[uid2][6] += 1
    
    return stats



startTime = time.time()
createMany(10, 2)
print(time.time() - startTime)