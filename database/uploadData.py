import mysql.connector
from dotenv import load_dotenv
import os
# set to "test_database" to upload to sample database
# set to "prod_db" for prod db


load_dotenv()
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
dataPath = ""
if DB_NAME == "prod_db":
    dataPath = "prodData"
else:
    dataPath = "sampleData"
# assume tables have been created and are empty

def load_data_into_table(table_name, file_path, sql_file_path):
    with open(sql_file_path, 'r') as file:
        query = file.read()
    

    # Replace placeholders with actual values
    query = query.format(table_name=table_name, file_path=file_path)
    return query

if __name__ == "__main__":
    conn = mysql.connector.connect(user=DB_USER, 
                              password=f"{DB_PASSWORD}", 
                              host=DB_HOST, 
                              port=3306, database=DB_NAME,
                              ssl_ca="DigiCertGlobalRootG2.crt.pem", 
                              ssl_disabled=False,
                              allow_local_infile=True)
    cursor = conn.cursor()

    dirname = os.path.dirname(__file__)
    queryPath = os.path.join(dirname, "sql", "upload.sql")


    # users
    userInfoPath = os.path.join(dirname, dataPath, "users.txt")
    cursor.execute("DELETE FROM `Users`;")
    query = load_data_into_table("Users", userInfoPath, queryPath)
    cursor.execute(query)

    # games
    gameDataPath = os.path.join(dirname, dataPath, "games.txt")
    cursor.execute("DELETE FROM `Games`;")
    query = load_data_into_table("Games", gameDataPath, queryPath)
    cursor.execute(query)
    stmt = "INSERT INTO Games (gid, uid1, uid2, final_game_state, result, start_time) VALUES (%s, %s, %s, %s, %s, %s)"
    stmt2 = "INSERT INTO Lobbies (gid, uid1, uid2, open) VALUES (%s, %s, %s, %s)"
    if DB_NAME == "prod_db":
        seq_params = [
            (10001, 6, None, None, None, None),
            (10002, 9, None, None, None, None),
            (10003, 4, None, None, None, None),
            (10004, 2, None, None, None, None),
            (10005, 0, None, None, None, None)
            ] 
        seq_params2 = [
            (10001, 6, None, True),
            (10003, 4, None, True),
            (10003, 4, None, True),
            (10004, 2, None, True),
            (10005, 0, None, True),
        ]
        cursor.executemany(stmt, seq_params)
        cursor.executemany(stmt2, seq_params2)
  
    else:
        seq_params = [
            (101, 6, None, None, None, None),
            (102, 9, None, None, None, None),
            ]
        seq_params2 = [
            (101, 6, None, True),
            (102, 9, None, True)
        ]
        cursor.executemany(stmt, seq_params)
        cursor.executemany(stmt2, seq_params2)

    # friends
    friendDataPath = os.path.join(dirname, dataPath, "friends.txt")
    cursor.execute("DELETE FROM `Friends`;")
    query = load_data_into_table("Friends", friendDataPath, queryPath)
    cursor.execute(query)

    # userStats
    userStatsPath = os.path.join(dirname, dataPath, "userStats.txt")
    cursor.execute("DELETE FROM `UserStats`;")
    query = load_data_into_table("UserStats", userStatsPath, queryPath)
    cursor.execute(query)

    #favourites
    favouritesPath = os.path.join(dirname, dataPath, "favourites.txt")
    cursor.execute("DELETE FROM `FavouriteGames`;")
    query = load_data_into_table("FavouriteGames", favouritesPath, queryPath)
    cursor.execute(query)

    #detailed moves
    detailedMovesPath = os.path.join(dirname, dataPath, "detailedMoves.txt")
    cursor.execute("DELETE FROM `detailedMoves`;")
    query = load_data_into_table("DetailedMoves", detailedMovesPath, queryPath)
    cursor.execute(query)

    #detailed moves
    detailedMovesPath = os.path.join(dirname, dataPath, "friendRequests.txt")
    cursor.execute("DELETE FROM `friendRequests`;")
    query = load_data_into_table("FriendRequests", detailedMovesPath, queryPath)
    cursor.execute(query)

    conn.commit()
    cursor.close()
    conn.close()

