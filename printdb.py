import sqlite3
import atexit

dbConnection = sqlite3.connect('moncafe.db')
cursor = dbConnection.cursor()


def close_db():
    dbConnection.commit()
    dbConnection.close()


atexit.register(close_db)


def print_list(list):
    for item in list:
        print(item)


def act():
    print("Activities")
    print_list(cursor.execute("""SELECT * FROM  Activities ORDER BY date ASC""").fetchall())
    print("Coffee stands")
    print_list(cursor.execute("""SELECT * FROM  Coffee_stands ORDER BY id ASC""").fetchall())
    print("Employees")
    print_list(cursor.execute("""SELECT * FROM  Employees ORDER BY id ASC""").fetchall())
    print("Products")
    print_list(cursor.execute("""SELECT * FROM  Products ORDER BY id ASC""").fetchall())
    print("Suppliers")
    print_list(cursor.execute("""SELECT * FROM  Suppliers ORDER BY id ASC""").fetchall())

    emp_report = cursor.execute("""
    SELECT emp.name, emp.salary, cs.location, 
		CASE
			WHEN sales.units > 0
				THEN SUM(sales.units * Products.price)
			ELSE 0
		END as total_sales
	FROM Employees as emp
	LEFT JOIN (SELECT *, SUM(act.quantity)*-1 as units
				FROM Activities as act
				WHERE act.quantity < 0
				GROUP BY act.activator_id, act.product_id) as sales
	ON sales.activator_id = emp.id
	LEFT JOIN Products ON Products.id = sales.product_id
	LEFT JOIN Coffee_stands as cs ON cs.id = emp.coffee_stand
	GROUP BY emp.id
	ORDER BY emp.name ASC 
    """)

    print("\nEmployees report")
    for emp in emp_report.fetchall():
        print(*emp)

    res = cursor.execute("""SELECT date,description, act.quantity, emp.name, sup.name
                            FROM Activities AS act
                            LEFT JOIN Products ON product_id = Products.id
                            LEFT JOIN Employees as emp ON emp.id = activator_id
                            LEFT JOIN Suppliers as sup ON sup.id = activator_id
                            ORDER BY date""").fetchall()

    if len(res) > 0 and (len(res[0]) > 0):
        print("\nActivities")
        print_list(res)


def main():
    act()


if __name__ == "__main__":
    main()
