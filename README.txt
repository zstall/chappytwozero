First unzip file in directory for project
Create a virtual environment
- With python3 create
    - ython3 -m venv venv
    - pip install twilio
    - pip install flask
    - pip install flask-restful

Create Database for Chappy:
- Edit your all_chores.csv to add or subtract chores. 
- Currently setup for daily and weekly chores
- Edit createChappyDB and add users. Can set any number of users
- When ready run: python createChappyDB.py

Setup twilio
- Link
- Update config.py file with twilio account info

Test chap.py
- Run chap.py comes in debug mode. Will output chores and people to command line
- Run with : python chap.py
- Turn off debug mode to send messages via twilio:
    - Set trace to False

Test fchap.py and api calls
- Run python fchap.py
- Will have a local host can run two api calls:
    - Mark chore done in DB: /choredone/<chr_name>
    - Reset daily or weekly chores: /resetchores/<sched>
