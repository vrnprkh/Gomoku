from secret import db_password

def getGames(uid):
    pass
def getFavourites(uid):
    pass
def setFavourites(uid, gid):
    pass
def removeFavourites(uid, gid):
    pass
def displayStats(uid):
    pass
def displayLeaderBoard(uid):
    pass

def main():
    currentUser = 0

    while True:
        print("Input command  (h for help): ")
        command = input()
        if command == "h":
            print("""Commands\n
                    h: help\n 
                    q: quit\n
                    u: set active user \n 
                    g: get games for user \n
                    f: get favourite games for user\n
                    sf: set favourite games for user\n
                    rf: remove favourite game for user\n
                    st: get stats for user\n
                    l: display leaderboard\n
                  """)
        elif command == "u":
            currentUser = int(input("Input uid:"))
        elif command == "q":
            break
        elif command == "g":
            print(getGames(currentUser))
        elif command == "f":
            print(getFavourites(currentUser))
        elif command == "sf":
            setFavourites(currentUser, int(input("gid to favourite: ")))
        elif command == "rf":
            removeFavourites(currentUser, int(input("gid to unfavourite: ")))
        elif command == "st":
            pass
        elif command == "l":
            pass



