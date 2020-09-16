import sqlite3
import csv
def create_database():

    try:
        sqliteConnection = sqlite3.connect('chappydb.db')
        cursor = sqliteConnection.cursor()
        print("Database created and Successfully Connected to SQLite")

        sqlite_select_query = 'SELECT sqlite_version();'
        cursor.execute(sqlite_select_query)
        record = cursor.fetchall()
        print("SQLite Database Version is: ", record)
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

def create_tables():
    try:
        sqliteConnection = sqlite3.connect('chappydb.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        with open('chappy_tables.sql', 'r') as sqlite_file:
            sql_script = sqlite_file.read()

        cursor.executescript(sql_script)
        print("SQLite script executed successfully")
        cursor.close()

    except sqlite3.Error as error:
        print("Error while executing sqlite script", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("sqlite connection is closed")

def insertUser(id, fname, lname, phone, email):
    try:
        sqliteConnection = sqlite3.connect('chappydb.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO users
                          (id, fname, lname, phone, email)
                          VALUES (?, ?, ?, ?, ?);"""

        data_tuple = (id, fname, lname, phone, email)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into users table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

def insertChores(choreList):
    try:
        sqliteConnection = sqlite3.connect('chappydb.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_query = """INSERT INTO chores
                          (id, chore, schedule, name, done)
                          VALUES (?, ?, ?, ?, ?);"""

        cursor.executemany(sqlite_insert_query, choreList)
        sqliteConnection.commit()
        print("Total", cursor.rowcount, "Records inserted successfully into chore table")
        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert multiple records into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

def get_chores_dic(file):

    rd = csv.reader(open(file))
    dic = {}

    for row in rd:
        key = row[0]
        dic[key] = row[1:]

    return dic

def main():

    trace = False

    create_database()
    create_tables()


    num = 1
    chrs = get_chores_dic('all_chores.csv')
    chrs_array = []
    for c in chrs['daily']:
        chrs_array.append((num, c, 'daily', 'null', 'False'))
        num += 1
    for c in chrs['weekly']:
        chrs_array.append((num, c, 'weekly', 'null', 'False'))
        num += 1

    if trace:
        print(chrs_array)

    else:
        insertUser(1, 'Zach', 'Stall', '9704203609', 'zstall4@gmail.com')
        insertUser(2, 'Caitlin', 'Kelly', '7209330451', 'caitlin.margaret.kelly@gmail.com')
        insertChores(chrs_array)


if __name__=="__main__":
    main()
