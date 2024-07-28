import mysql.connector
from mysql.connector import Error
from datetime import datetime

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='taste_user',
            password='wine',
            database='Bacchus'
        )
        if connection.is_connected():
            print("Connected to Bacchus database")
        return connection
    except Error as e:
        print(f"Error: '{e}' occurred")
        return None

def get_distributor_column_names(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("DESCRIBE distributor")
        columns = cursor.fetchall()
        return [column[0] for column in columns]
    except Error as e:
        print(f"Error: '{e}' occurred while fetching distributor column names")
        return None

def fetch_distributor_wine_sales(connection, distributor_name_column):
    try:
        cursor = connection.cursor()
        query = f"""
        SELECT DISTINCT 
            distributor.{distributor_name_column}, 
            wine.wine_name, 
            wine.wine_sold
        FROM distributor
        JOIN delivery ON distributor.distributor_id = delivery.distributor_id
        JOIN orders ON delivery.delivery_id = orders.delivery_id
        JOIN wine ON orders.wine_id = wine.wine_id
        ORDER BY distributor.{distributor_name_column}, wine.wine_name;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            print("No distributor-wine relationships found.")
        else:
            print("\nDistributor-Wine Sales:")
            print("-" * 50)
            distributor_col = max(len('Distributor'), max(len(str(row[0])) for row in results))
            wine_col = max(len('Wine'), max(len(str(row[1])) for row in results))
            sold_col = max(len('Wines Sold'), max(len(str(row[2])) for row in results))

            print(f"{'Distributor':<{distributor_col + 2}} {'Wine':<{wine_col + 2}} {'Wines Sold':<{sold_col + 2}}")
            print("-" * (distributor_col + wine_col + sold_col + 6))

            for row in results:
                distributor, wine, wines_sold = row
                print(f"{distributor:<{distributor_col + 2}} {wine:<{wine_col + 2}} {wines_sold:<{sold_col + 2}}")

    except Error as e:
        print(f"Error: '{e}' occurred while fetching the distributor-wine relationships")

def fetch_customer_delivery(connection, distributor_name_column):
    try:
        cursor = connection.cursor()
        query = f"""
        SELECT delivery.delivery_name, wine.wine_name AS wine_name, distributor.{distributor_name_column}, 
               delivery.expected_date, delivery.actual_date
        FROM delivery
        JOIN distributor ON delivery.distributor_id = distributor.distributor_id
        JOIN orders ON delivery.delivery_id = orders.delivery_id
        JOIN wine ON orders.wine_id = wine.wine_id;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            print("No delivery data found.")
        else:
            print("\n\nCustomer Delivery:")
            print("-" * 50)
            delivery_name_col = max(len('Delivery Name'), max(len(str(row[0])) for row in results))
            wine_name_col = max(len('Wine Name'), max(len(str(row[1])) for row in results))
            distributor_name_col = max(len('Distributor Name'), max(len(str(row[2])) for row in results))
            expected_date_col = max(len('Expected Date'), max(len(format_date(row[3])) for row in results))
            actual_date_col = max(len('Actual Delivery Date'), max(len(format_date(row[4])) for row in results))

            header = (f"{'Delivery Name':<{delivery_name_col + 2}} {'Wine Name':<{wine_name_col + 2}} "
                      f"{'Distributor Name':<{distributor_name_col + 2}} {'Expected Date':<{expected_date_col + 2}} "
                      f"{'Actual Delivery Date':<{actual_date_col + 2}}")
            print(header)
            print('-' * len(header))

            for row in results:
                delivery_name, wine_name, distributor_name, expected_date, actual_date = row
                print(f"{delivery_name:<{delivery_name_col + 2}} {wine_name:<{wine_name_col + 2}} "
                      f"{distributor_name:<{distributor_name_col + 2}} {format_date(expected_date):<{expected_date_col + 2}} "
                      f"{format_date(actual_date):<{actual_date_col + 2}}")

    except Error as e:
        print(f"Error: '{e}' occurred while fetching the customer's delivery details")

def fetch_employee_hours(connection):
    try:
        cursor = connection.cursor()
        query = """
        SELECT employee.employee_lastname, employee.employee_hours, employee.employee_position
        FROM employee
        """
        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            print("No employee data found.")
        else:
            print("\n\nEmployee Hours:")
            print("-" * 50)
            employee_lastname_col = max(len('Employee Last Name'), max(len(str(row[0])) for row in results))
            employee_hours_col = max(len('Hours Worked'), max(len(str(row[1])) for row in results))
            employee_position_col = max(len('Employee Position'), max(len(str(row[2])) for row in results))

            header = (f"{'Employee Last Name':<{employee_lastname_col + 2}} "
                      f"{'Hours Worked':<{employee_hours_col + 2}} {'Employee Position':<{employee_position_col + 2}}")
            print(header)
            print('-' * len(header))

            for row in results:
                employee_lastname, employee_hours, employee_position = row
                print(f"{employee_lastname:<{employee_lastname_col + 2}} "
                      f"{employee_hours:<{employee_hours_col + 2}} {employee_position:<{employee_position_col + 2}}")

    except Error as e:
        print(f"Error: '{e}' occurred while fetching the employee hours")

def format_date(date):
    return date.strftime('%m-%d-%Y') if date else ''

def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("\nMySQL connection is closed")

def main():
    connection = create_connection()
    if connection:
        distributor_columns = get_distributor_column_names(connection)
        if distributor_columns:
            distributor_name_column = next((col for col in distributor_columns if 'name' in col.lower()), None)
            if distributor_name_column:
                fetch_distributor_wine_sales(connection, distributor_name_column)
                fetch_customer_delivery(connection, distributor_name_column)
                fetch_employee_hours(connection)
            else:
                print("Could not find a column for distributor name")
        close_connection(connection)

if __name__ == "__main__":
    main()