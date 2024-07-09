import mysql.connector
from secret import db_password
import os
# set to "test_database" to upload to sample database
# set to "prod_db" for prod db
DB_NAME = "prod_db"
dataPath = ""
if DB_NAME == "prod_db":
    dataPath = "prodData/"
else:
    dataPath = "sampleData/"
# assume tables have been created and are empty

def load_data_into_table(table_name, file_path, sql_file_path):
    with open(sql_file_path, 'r') as file:
        query = file.read()
    

    # Replace placeholders with actual values
    query = query.format(table_name=table_name, file_path=file_path)
    return query

if __name__ == "__main__":
    conn = mysql.connector.connect(user="gomoku_db_admin", 
                              password=f"{db_password}", 
                              host="gomoku-database.mysql.database.azure.com", 
                              port=3306, database=DB_NAME,
                              ssl_ca="DigiCertGlobalRootG2.crt.pem", 
                              ssl_disabled=False,
                              allow_local_infile=True)
    cursor = conn.cursor()

    dirname = os.path.dirname(__file__)
    queryPath = os.path.join(dirname, "sql/upload.sql")
    


    # users
    userInfoPath = os.path.join(dirname, dataPath + "users.txt")
    cursor.execute("DELETE FROM `Users`;")
    query = load_data_into_table("Users", userInfoPath, queryPath)
    cursor.execute(query)

    # games
    gameDataPath = os.path.join(dirname, dataPath + "games.txt")
    cursor.execute("DELETE FROM `Games`;")
    query = load_data_into_table("Games", gameDataPath, queryPath)
    cursor.execute(query)

    # friends
    friendDataPath = os.path.join(dirname, dataPath + "friends.txt")
    cursor.execute("DELETE FROM `Friends`;")
    query = load_data_into_table("Friends", friendDataPath, queryPath)
    cursor.execute(query)

    # userStats
    userStatsPath = os.path.join(dirname, dataPath + "userStats.txt")
    cursor.execute("DELETE FROM `UserStats`;")
    query = load_data_into_table("UserStats", userStatsPath, queryPath)
    cursor.execute(query)

    #favourites
    favouritesPath = os.path.join(dirname, dataPath + "favourites.txt")
    cursor.execute("DELETE FROM `FavouriteGames`;")
    query = load_data_into_table("FavouriteGames", favouritesPath, queryPath)
    cursor.execute(query)

    #detailed moves
    detailedMovesPath = os.path.join(dirname, dataPath + "detailedMoves.txt")
    cursor.execute("DELETE FROM `detailedMoves`;")
    query = load_data_into_table("DetailedMoves", detailedMovesPath, queryPath)
    cursor.execute(query)

    #detailed moves
    detailedMovesPath = os.path.join(dirname, dataPath + "friendRequests.txt")
    cursor.execute("DELETE FROM `friendRequests`;")
    query = load_data_into_table("FriendRequests", detailedMovesPath, queryPath)
    cursor.execute(query)

    conn.commit()
    cursor.close()
    conn.close()

