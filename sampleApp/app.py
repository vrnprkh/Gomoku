from backend.secret import db_password
import mysql.connector
import os

def readQuery(queryName):
    dirname = os.path.dirname(__file__)
    sql_file_path = os.path.join(dirname, "templates", queryName)
    query = ""
    with open(sql_file_path, 'r') as file:
        query = file.read()
    return query

def getGames(uid):
    #setup
    conn = mysql.connector.connect(user="gomoku_db_admin", 
                              password=f"{db_password}", 
                              host="gomoku-database.mysql.database.azure.com", 
                              port=3306, database="test_database", 
                              ssl_ca="DigiCertGlobalRootG2.crt.pem", 
                              ssl_disabled=False,
                              allow_local_infile=True)
    cursor = conn.cursor()

    # query
    query = readQuery("getGames.sql")
    query = query.format(player1=uid)
    cursor.execute(query)
    result = "\n".join(map(str,cursor.fetchall()))
    #cleanup
    cursor.close()
    conn.close()
    return result

def getFavourites(uid):
    #setup
    conn = mysql.connector.connect(user="gomoku_db_admin", 
                              password=f"{db_password}", 
                              host="gomoku-database.mysql.database.azure.com", 
                              port=3306, database="test_database", 
                              ssl_ca="DigiCertGlobalRootG2.crt.pem", 
                              ssl_disabled=False,
                              allow_local_infile=True)
    cursor = conn.cursor()
    # query
    query = readQuery("getFavourites.sql")
    query = query.format(player1=uid)
    cursor.execute(query)
    result = "\n".join(map(str,cursor.fetchall()))
    #cleanup
    cursor.close()
    conn.close()
    return result

def setFavourites(uid, gid):
    #setup
    conn = mysql.connector.connect(user="gomoku_db_admin", 
                              password=f"{db_password}", 
                              host="gomoku-database.mysql.database.azure.com", 
                              port=3306, database="test_database", 
                              ssl_ca="DigiCertGlobalRootG2.crt.pem", 
                              ssl_disabled=False,
                              allow_local_infile=True)
    cursor = conn.cursor()
    # query
    query = readQuery("setFavourite.sql")
    query = query.format(player1=uid, favGID=gid)
    cursor.execute(query)
    result = "\n".join(map(str,cursor.fetchall()))
    #cleanup
    conn.commit() # modifying data
    cursor.close()
    conn.close()
    return result
def removeFavourites(uid, gid):
    #setup
    conn = mysql.connector.connect(user="gomoku_db_admin", 
                              password=f"{db_password}", 
                              host="gomoku-database.mysql.database.azure.com", 
                              port=3306, database="test_database", 
                              ssl_ca="DigiCertGlobalRootG2.crt.pem", 
                              ssl_disabled=False,
                              allow_local_infile=True)
    cursor = conn.cursor()
    # query
    query = readQuery("removeFavourite.sql")
    query = query.format(player1=uid, favGID=gid)
    cursor.execute(query)
    result = "\n".join(map(str,cursor.fetchall()))
    #cleanup
    conn.commit() # modifying data
    cursor.close()
    conn.close()
    return result

def displayLeaderBoard():
        #setup
    conn = mysql.connector.connect(user="gomoku_db_admin", 
                              password=f"{db_password}", 
                              host="gomoku-database.mysql.database.azure.com", 
                              port=3306, database="test_database", 
                              ssl_ca="DigiCertGlobalRootG2.crt.pem", 
                              ssl_disabled=False,
                              allow_local_infile=True)
    cursor = conn.cursor()
    # query
    query = readQuery("displayLeaderboard.sql")
    cursor.execute(query)
    result = "\n".join(map(str,cursor.fetchall()))
    #cleanup
    cursor.close()
    conn.close()
    return result

def displayOpenLobbies():
            #setup
    conn = mysql.connector.connect(user="gomoku_db_admin", 
                              password=f"{db_password}", 
                              host="gomoku-database.mysql.database.azure.com", 
                              port=3306, database="test_database", 
                              ssl_ca="DigiCertGlobalRootG2.crt.pem", 
                              ssl_disabled=False,
                              allow_local_infile=True)
    cursor = conn.cursor()
    # query
    query = readQuery("searchAllLobbies.sql")
    cursor.execute(query)
    result = "\n".join(map(str,cursor.fetchall()))
    #cleanup
    cursor.close()
    conn.close()
    return result


def openFriendLobbies(uid):
            #setup
    conn = mysql.connector.connect(user="gomoku_db_admin", 
                              password=f"{db_password}", 
                              host="gomoku-database.mysql.database.azure.com", 
                              port=3306, database="test_database", 
                              ssl_ca="DigiCertGlobalRootG2.crt.pem", 
                              ssl_disabled=False,
                              allow_local_infile=True)
    cursor = conn.cursor()
    # query
    query = readQuery("openFriendLobbies.sql")
    query = query.format(player = uid)
    cursor.execute(query)
    result = "\n".join(map(str,cursor.fetchall()))
    #cleanup
    cursor.close()
    conn.close()
    return result

def main():
    currentUser = 0

    while True:
        print("Input command  (h for help): ")
        command = input()
        if command == "h":
            print("""Commands
                    h: help
                    q: quit
                    u: set active user
                    g: get games for user
                    f: get favourite games for user
                    sf: set favourite games for user
                    rf: remove favourite game for user
                    l: display leaderboard
                    o: display open lobbies
                    fo: display open lobbies of friends
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
        elif command == "l":
            print(displayLeaderBoard())
        elif command == "o":
            print(displayOpenLobbies())
        elif command == "fo":
            print(openFriendLobbies(currentUser))
        


if __name__ == "__main__":
    main()