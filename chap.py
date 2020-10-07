#!/home/ec2-user/venv/python3/bin/python

"""
Author: Zachary Stall
Date: 9/13/2020
Description: The start of chore app. Using a sqlite db, and hopefully a flask,
this application will allow a user to get randomly selected chores assigned to
them daily, weekly, and monthly.

This particular file is a collection of functions to access and update the DB.
"""

# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import csv
import datetime
import random
import config
import sys
import sqlite3


# Send a message using twilio. The follow vars are needed:
#   chr     - array of Chores
#   nm      - str name of user
#   phone   - str phone number of user
#   wchr    - array of weekly chores
#   Day     - string var of which day of the week it is, Mon - 0 Sunday - 6
#   trace   - trace is a var for debugging defaults to False

def send_message(chr, nm, phone, wchr, day, trace=False):

    # client config information for twilio for config file
    client = Client(config.account_sid, config.auth_token)

    # Building the message for the users
    msg = '****************************************' + '\n'
    msg += nm + ' here are your Chores: '

    for i in chr:
        msg += '\n' + '- ' + i[1]

    if day == 0:
        msg += '\n' + '****************************************'
        msg += '\n' 'Here is your weekly chores:'
        for i in wchr:
            msg += '\n' + '- ' + i[1]
    else:

        msg += '\n' + '****************************************'
        msg += '\n' "Don't forget your weekly chores: "
        for i in wchr:
            msg += '\n' + '- ' + i[1]

    msg += '\n' + '****************************************'

    # debugging if trace true will print message to command line
    if trace:
        print()
        print("*********** MESSAGE DEBUG **************")
        print(msg)
        print("********* END MESSAGE DEBUG ************")
        print()

    # if trace is false, send message!
    else:
        message = client.messages \
            .create(
                body=msg,
                from_='+19704239976',
                to=phone
            )

        print(message.status)

# pass in any query statement to this function and it will return the results
# tables are:
#    users
#       columns: id, fname, lname, phone, email
#    chores
#       columns: id, chore, schedule, name, done

def query_db(select_statement, trace=False):
    try:
        sqliteConnection = sqlite3.connect('chappydb.db')
        cursor = sqliteConnection.cursor()
        if trace:
            print("Connected to SQLite")

        sqlite_select_query = select_statement
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        if trace:
            print("Total rows are:  ", len(records))
            print("Printing each query result")
            print(records)
        cursor.close()
        return records

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            if trace:
                print("The SQLite connection is closed")



def update_db(update_statement, trace=False):
    try:
        sqliteConnection = sqlite3.connect('chappydb.db')
        cursor = sqliteConnection.cursor()
        if trace:
            print("Connected to SQLite")

        sql_update_query = update_statement
        cursor.execute(sql_update_query)
        sqliteConnection.commit()
        if trace:
            print("Record Updated successfully ")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            if trace:
                print("The SQLite connection is closed")

def chore_done(chr_name):
    chr = query_db("SELECT * FROM chores WHERE chore = '" + chr_name + "'")
    print(chr)
    if chr[0][4] == 'False':
        update_db("UPDATE chores set done = 'True' WHERE id = " + str(chr[0][0]))
    else:
        update_db("UPDATE chores set done = 'False' WHERE id = " + str(chr[0][0]))
    return query_db("SELECT * FROM chores WHERE chore = '" + chr_name + "'")

# Build randomly assign user chores, but updating chores table name category with users
# inputs -  chrs array of chores from selec * from db
#           users array of users from select * from db
def build_user_chores(chrs, users, trace = False):

    num = chrs[0][0]
    chrs_ids = []
    while num <= chrs[len(chrs)-1][0]:
        chrs_ids.append(num)
        num += 1

    usr_names = []
    for u in users:
        usr_names.append(u[1])

    while len(chrs_ids) > 0:
        for name in usr_names:
            if chrs_ids == []:
                break
            chr_id = chrs_ids.pop(random.randint(0,len(chrs_ids)-1))
            add_name = "UPDATE chores SET name = '"+str(name)+"' where id = " + str(chr_id)
            update_db(add_name, trace)

# Clear or refresh names column in chore table
def clear_chore_names(sched):
    remove_names = "UPDATE chores SET name = '' where schedule = '" + sched + "'"
    update_db(remove_names)

def reset_chores(sched):
    reset_chores = "UPDATE chores SET done = 'False' WHERE schedule = '" + sched + "'"
    update_db(reset_chores)
    return(query_db("SELECT * FROM chores"))

def main():
    trace = False
    reset_chores('daily')
    # Get array of users; (id, fname, lname, phone, email)
    usr = query_db("select * from users", trace)
    # Get array of daily chores (id, chores, interval, done (true or false))
    chrs = query_db("select * from chores where schedule = 'daily'", trace)
    # Get day of the week Monday = 0 Sunday = 6
    day = datetime.datetime.today().weekday()
    # Add names to chores for the week
    build_user_chores(chrs, usr)

    if day == 1:
        reset_chores('weekly')
        wk_chrs = query_db("select * from chores where schedule = 'weekly'", trace)
        build_user_chores(wk_chrs, usr)

    for u in usr:
        chrs = query_db("SELECT * FROM chores where name = '" + str(u[1]) + "' and schedule = 'daily'")
        wk_chrs = query_db("SELECT * FROM chores where name = '" + str(u[1]) + "' and schedule = 'weekly'")
        send_message(chrs, u[1], u[3], wk_chrs, day, True)


if __name__=="__main__":
    main()
