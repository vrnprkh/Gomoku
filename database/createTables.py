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
    queryPath = os.path.join(dirname, "sql/create.sql")
    query = None
    with open(queryPath, 'r') as file:
        query = file.read()
    cursor.execute(query)
    
    conn.commit()
    cursor.close()
    conn.close()
 


    