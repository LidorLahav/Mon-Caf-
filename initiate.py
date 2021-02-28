import sqlite3
import os
import atexit
import sys


def close_db():
    dbConnection.commit()
    dbConnection.close()


def create_tables():
    cursor.execute("""CREATE TABLE Employees(
                    id      INTEGER PRIMARY KEY,
                    name    TEXT NOT NULL,
                    salary  REAL NOT NULL,
                    coffee_stand INTEGER REFERENCES Coffee_stands(id))""")

    cursor.execute("""CREATE TABLE Suppliers(
                    id                  INTEGER PRIMARY KEY,
                    name                TEXT NOT NULL,
                    contact_information TEXT)""")

    cursor.execute("""CREATE TABLE Products(
                    id          INTEGER PRIMARY KEY,
                    description TEXT NOT NULL,
                    price       REAL NOT NULL,
                    quantity    INTEGER NOT NULL)""")

    cursor.execute("""CREATE TABLE Coffee_stands(
                    id                  INTEGER PRIMARY KEY,
                    location            TEXT NOT NULL,
                    number_of_employees INTEGER)""")

    cursor.execute("""CREATE TABLE Activities(
                    product_id      INTEGER INTEGER REFERENCES Products(id),
                    quantity        INTEGER NOT NULL,
                    activator_id    INTEGER NOT NULL,
                    date            DATE NOT NULL)""")


def insert_row(row):
    row = row.split(", ")
    if row[0] == 'E':
        cursor.execute("INSERT INTO Employees VALUES (?,?,?,?)", (row[1], row[2], row[3], row[4]))
    elif row[0] == 'S':
        if len(row) == 4:
            cursor.execute("INSERT INTO Suppliers VALUES (?,?,?)", (row[1], row[2], row[3]))
        else:
            cursor.execute("INSERT INTO Suppliers VALUES (?,?,NULL)", (row[1], row[2]))
    elif row[0] == 'P':
        cursor.execute("INSERT INTO Products VALUES (?,?,?,?)", (row[1], row[2], row[3], 0))
    elif row[0] == 'C':
        if len(row) == 4:
            cursor.execute("INSERT INTO Coffee_stands VALUES (?,?,?)", (row[1], row[2], row[3]))
        else:
            cursor.execute("INSERT INTO Coffee_stands VALUES (?,?,NULL)", (row[1], row[2]))


def insert_data():
    with open(sys.argv[1]) as file:
        content = file.readlines()
        for row in content:
            insert_row(row.strip())


def main():
    create_tables()
    insert_data()


DBExist = os.path.isfile('moncafe.db')
if DBExist:
    os.remove('moncafe.db')
dbConnection = sqlite3.connect('moncafe.db')
cursor = dbConnection.cursor()
atexit.register(close_db)
main()

