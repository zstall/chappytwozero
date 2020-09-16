# Update Chappy app
Chappy now uses sqlite for a db and has some api functionality. Will need to do some more cleanup here, but wanted to get the ball rolling.
For more general Chappy informatoin and setup (setting up Twilio and running Chappy in a ec2 environment) please review the setup steps [here](https://github.com/zstall/chappy)

**NOTE** for testing, to quiet down the debugging output, instead of setting trace = True, in chap.py on line 194 I hardcoded trace to True.
`send_message(chrs, u[1], u[3], wk_chrs, day, True)`

**NOTE** this will print out the messages to the command line, and NOT send any sms messages through Twilio. Should change True to trace, and use the trace variable after done testing.

## Step 1: Create a virtual environment
With python3 create 
- python3 -m venv venv
- source venv/bin/activate
Install dependencies
- pip install twilio
- pip install flask
- pip install flask-restful

## Step 2: Create Database for Chappy:
- Edit your all_chores.csv to add or subtract chores. 
- Currently setup for daily and weekly chores
- Edit createChappyDB and add users. Can set any number of users
- When ready run: python createChappyDB.py

## Step 3: Setup twilio
- [Review twilio setup here](https://github.com/zstall/chapp)
- Update config.py file with twilio account info

## Step 4: Test chap.py
- Run chap.py comes in debug mode. Will output chores and people to command line
- Run with : python chap.py
- Turn off debug mode to send messages via twilio:
    - Set trace to False

## Step 5: Test fchap.py and api calls
- Run python fchap.py
- Will have a local host can run two api calls:
    - Mark chore done in DB: /choredone/<chr_name>
    - Reset daily or weekly chores: /resetchores/<sched>
