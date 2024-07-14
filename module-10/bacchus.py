import mysql.connector
from mysql.connector import Error

def connect():
    """ Connect to MySQL database """
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            database='bacchus',  
            user='taste_user',  
            password='wine'
        )
        if conn.is_connected():
            print('Connected to MySQL database')
            return conn
    except Error as e:
        print(e)

def fetch_and_print_results(conn, query, description, columns):
    """ Fetch the results for a given query and print them """
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        print(f"\n-- {description} --")
        for row in result:
            for col, value in zip(columns, row):
                print(f"{col}: {value}")
            print("\n")
    except Error as e:
        print(f"Error: '{e}'")

def main():
    # Step 1: Connect to the database
    conn = connect()
    
    if conn:
        # Step 2: Query 1 - Select all fields from the wine table
        fetch_and_print_results(conn, 
                                "SELECT wine_id, wine_type FROM wine", 
                                "DISPLAYING Wine RECORDS", 
                                ["Wine ID", "Wine Type"])

        # Step 3: Query 2 - Select all fields from the supplier table
        fetch_and_print_results(conn, 
                                "SELECT supplier_id, supplier_name, supply_type FROM supplier", 
                                "DISPLAYING Supplier RECORDS", 
                                ["Supplier ID", "Supplier Name", "Supply Type"])

        # Step 4: Query 3 - Select all fields from the inventory table
        fetch_and_print_results(conn, 
                                "SELECT inventory_id, quantity, supply_type, supplier_id FROM inventory", 
                                "DISPLAYING Inventory RECORDS", 
                                ["Inventory ID", "Quantity", "Supply Type", "Supplier ID"])

        # Step 5: Query 4 - Select all fields from the deliveries table
        fetch_and_print_results(conn, 
                                "SELECT delivery_id, supplier_id, delivery_name, expected_date, actual_date FROM deliveries", 
                                "DISPLAYING Delivery RECORDS", 
                                ["Delivery ID", "Supplier ID", "Delivery Name", "Expected Date", "Actual Date"])

        # Step 6: Query 5 - Select all fields from the orders table
        fetch_and_print_results(conn, 
                                "SELECT orders_id, inventory_id, supplier_id, order_date, delivery_id, wine_id FROM orders", 
                                "DISPLAYING Order RECORDS", 
                                ["Order ID", "Inventory ID", "Supplier ID", "Order Date", "Delivery ID", "Wine ID"])

        # Step 7: Query 6 - Select all fields from the employee table
        fetch_and_print_results(conn, 
                                "SELECT employee_id, employee_firstname, employee_lastname, employee_hours, employee_position FROM employee", 
                                "DISPLAYING Employee RECORDS", 
                                ["Employee ID", "First Name", "Last Name", "Hours", "Position"])

        # Step 8: Query 7 - Select all fields from the department table
        fetch_and_print_results(conn, 
                                "SELECT department_id, department_name, employee_id FROM department", 
                                "DISPLAYING Department RECORDS", 
                                ["Department ID", "Department Name", "Employee ID"])

        conn.close()

if __name__ == "__main__":
    main()