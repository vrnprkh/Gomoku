import mysql.connector
import os
import getpass

def get_password():
    return getpass.getpass("Enter the database password: ")

def execute_sql_file(cursor, sql_file_path, output_dir):
    with open(sql_file_path, 'r') as file:
        query = file.read()

    for result in cursor.execute(query, multi=True):
        if result.with_rows:
            results = result.fetchall()
            column_names = [i[0] for i in result.description]

            output_file_path = os.path.join(output_dir, os.path.basename(sql_file_path).replace('.sql', '.out'))
            with open(output_file_path, 'w') as out_file:
                out_file.write("\t".join(column_names) + "\n")
                for row in results:
                    out_file.write("\t".join(str(col) for col in row) + "\n")
            print(f"Output written to {output_file_path}")

if __name__ == "__main__":
    db_password = get_password()
    base_dir = os.path.dirname(__file__)

    ca_cert_path = os.path.join(base_dir, '../../helloworld/DigiCertGlobalRootG2.crt.pem')
    if not os.path.exists(ca_cert_path):
        raise FileNotFoundError(f"The CA certificate file was not found at path: {ca_cert_path}")

    conn = mysql.connector.connect(
        user="gomoku_db_admin", 
        password=db_password, 
        host="gomoku-database.mysql.database.azure.com", 
        port=3306, 
        database="test_database", 
        ssl_ca=ca_cert_path, 
        ssl_disabled=False
    )

    cursor = conn.cursor()

    directories = [
        os.path.join(base_dir, "r6"),
        os.path.join(base_dir, "r8"),
        os.path.join(base_dir, "r9")
    ]
    output_dir = os.path.join(base_dir, "output_files")
    os.makedirs(output_dir, exist_ok=True)

    for directory in directories:
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                if filename.endswith(".sql"):
                    sql_file_path = os.path.join(directory, filename)
                    execute_sql_file(cursor, sql_file_path, output_dir)
        else:
            print(f"Directory does not exist: {directory}")

    cursor.close()
    conn.close()
