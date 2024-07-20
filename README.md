# Gomoku⚪⚫
## Technologies & design
![Tech](/assets/tech.png)
## Current UI
![Gameplay](/assets/gamePlay.png)
![Statistics](/assets/stats.png)
![Match-History](/assets/match-history.png)
![Log-in](/assets/Log-in.png)
![Sign-up](/assets/Sign-up.png)
![About](/assets/about.png)


## Current Supported Features
- User Account Creation (with encrypted passwords), Account login, and changing / logging out of accounts. (Not a rubric feature)
- Searching for users by username, either searching all users, or searching from friends only. (R9)
- Match history, and Favourite games of the logged in user. (R7)
- Viewing aggregate stats of a user (R8), such as wins, losses, games played, and total time in game.

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
- create a .env with the following information
    ```
    DB_USER={db_username}
    DB_PASSWORD={db_password}
    DB_HOST={domain}.mysql.database.azure.com
    DB_NAME={db_name}
    SECRET_KEY={key}
    JWT_SECRET_KEY={key}
    ```
- Note the SECRET_KEY is for flask and can be arbritrary
- JWT_SECRET_KEY is for user tokens, and is also arbritrary
- create and activate a venv
- install all requirements with pip
- run the app with `python run.py`
5. Run frontend
- Navigate to frontend/my-app
- run `npm install`
- run `npm start`

The app should now be functional!




