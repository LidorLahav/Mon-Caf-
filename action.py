import sqlite3
import atexit
import sys
import printdb


def close_action():
    dbConnection.commit()
    dbConnection.close()
    printdb.act()


def act(product_id, quantity, activator_id, date):
    tmp = cursor.execute("""
        SELECT quantity 
        FROM Products
        WHERE Products.id = ?""", [product_id]).fetchone()
    if int(tmp[0]) + int(quantity) >= 0:
        insert_row(product_id, quantity, activator_id, date)
    cursor.execute("""
    UPDATE Products SET quantity = CASE
    WHEN (quantity + ?) >= 0
        THEN quantity + ?
        ELSE
            quantity
        END
    WHERE id = ?""", [quantity, quantity, product_id])


def insert_row(product_id, quantity, activator_id, date):
    cursor.execute("""
    INSERT INTO Activities 
    VALUES (?,?,?,?)""", [product_id, quantity, activator_id, date])


def main():
    with open(sys.argv[1]) as file:
        content = file.readlines()
        for row in content:
            [product_id, quantity, activator_id, date] = row.strip().split(", ")
            act(product_id, quantity, activator_id, date)


dbConnection = sqlite3.connect("moncafe.db")
cursor = dbConnection.cursor()
atexit.register(close_action)
main()
