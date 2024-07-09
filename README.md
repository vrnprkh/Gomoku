# Gomoku⚪⚫
## Current UI
![Log-in](/assets/Log-in.png)
![Sign-up](/assets/Sign-up.png)
![Gameplay](/assets/gamePlay.png)
![About](/assets/about.png)
![Profile](/assets/profile.png)

## Prerequisites
-------------
- Active Azure subscription
- Azure Database for MySQL server: A MySQL server needs to be set up in your Azure portal
- Python and npm

# Step 1: Creating the Sample Database
------------------------------------
1. Log in to Azure Portal.

2. Create a MySQL Database, named "test_database", or "prod_db". By default, test_database will only contain sample data (10 users, 100 games) (using the upload script), and prod_db will contain a signifcantly larger set of (1000 users, 10000 games). 
3. Once the database has been created, navigate to "database/". In here do the following:
- create a .env file with the following values:
    ```
    DB_USER={db_username}
    DB_PASSWORD={db_password}
    DB_HOST={domain}.mysql.database.azure.com
    DB_NAME={db_name}
    ```
- Create a virtual environment (`python -m venv venv`) and activate (platform dependent)
- install dependencies on venv (`pip install -r requirements.txt`)
- create tables using createTables.py (`python createTables.py`)
- uploadData using uploadData.py (`python uploadData.py`)

4. Run backend
- Navigate to backend/
- create and activate a venv
- install all requirements with pip
- run the app with `python run.py`
5. Run frontend
- Navigate to frontend/my-app
- run `npm install`
- run `npm start`

The app should now be functional!

