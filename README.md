# Gomoku⚪⚫
## Current UI
![Sign-up](/assets/Sign-up.png)
![Gameplay](/assets/gamePlay.png)
![About](/assets/about.png)
![Profile](/assets/profile.png)

## Prerequisites
-------------
- Active Azure subscription
- Azure Database for MySQL server: A MySQL server needs to be set up in your Azure portal
- Python & required libraries (`mysql-connector-python`)

# Step 1: Creating the Sample Database
------------------------------------
1. Log in to Azure Portal.

2. Create a MySQL Database, named "<database name>".

3. Set Up Database Tables by using create.sql (under database/sql/create.sql) This creates all the tables with the current constraints needed. To load the data into the tables, run the uploader.py script under database/. This will fill the tables with all the data in sampleData directory. To generate new data, use the dataGenerator.py script, which will create randomly generated data, for n users. Currently the data generated includes: Users, Completed Games (Games Table), Friends, and userStats. Lobbies are manually created in sampleData to test a feature. As of now, this is the data needed for our sample features and tests, the remaining tables will be populated for future milestones.
