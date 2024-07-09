import mysql.connector
from backend.instance.secret import db_password
import os
# assume tables have been created and are empty

def load_data_into_table(table_name, file_path, sql_file_path):
    with open(sql_file_path, 'r') as file:
        query = file.read()
    

    # Replace placeholders with actual values
    query = query.format(table_name=table_name, file_path=file_path)
    return query

    print(f"Data loaded successfully into {table_name}")

if __name__ == "__main__":
    conn = mysql.connector.connect(user="gomoku_db_admin", 
                              password=f"{db_password}", 
                              host="gomoku-database.mysql.database.azure.com", 
                              port=3306, database="test_database", 
                              ssl_ca="DigiCertGlobalRootG2.crt.pem", 
                              ssl_disabled=False,
                              allow_local_infile=True)
    cursor = conn.cursor()

    dirname = os.path.dirname(__file__)
    queryPath = os.path.join(dirname, "sql/upload.sql")
    


    # users
    userInfoPath = os.path.join(dirname, "sampleData/userData.txt")
    cursor.execute("DELETE FROM `Users`;")
    query = load_data_into_table("Users", userInfoPath, queryPath)
    cursor.execute(query)

    # games
    gameDataPath = os.path.join(dirname, "sampleData/gameData.txt")
    cursor.execute("DELETE FROM `Games`;")
    query = load_data_into_table("Games", gameDataPath, queryPath)
    cursor.execute(query)

    # friends
    friendDataPath = os.path.join(dirname, "sampleData/friends.txt")
    cursor.execute("DELETE FROM `Friends`;")
    query = load_data_into_table("Friends", friendDataPath, queryPath)
    cursor.execute(query)

    # userStats
    userStatsPath = os.path.join(dirname, "sampleData/userStats.txt")
    cursor.execute("DELETE FROM `UserStats`;")
    query = load_data_into_table("UserStats", userStatsPath, queryPath)
    cursor.execute(query)

    lobbiesPath = os.path.join(dirname, "sampleData/lobbies.txt")
    cursor.execute("DELETE FROM `LOBBIES`;")
    query = load_data_into_table("Lobbies", lobbiesPath, queryPath)
    cursor.execute(query)

    conn.commit()
    cursor.close()
    conn.close()

