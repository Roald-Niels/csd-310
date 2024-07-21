import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Establish connection to the MySQL database
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

# Fetch and print delivery details
def fetch_delivery_details(connection):
    try:
        cursor = connection.cursor()
        query = """
        SELECT deliveries.delivery_name, wine.wine_type AS wine_name, supplier.supplier_name, 
               deliveries.expected_date, deliveries.actual_date
        FROM deliveries
        JOIN orders ON deliveries.delivery_id = orders.delivery_id
        JOIN wine ON orders.wine_id = wine.wine_id
        JOIN supplier ON deliveries.supplier_id = supplier.supplier_id;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            print("No delivery data found.")
        else:
            # Find the maximum width of each column
            delivery_name_col = max(len('Delivery Name'), max(len(str(row[0])) for row in results))
            wine_name_col = max(len('Wine Name'), max(len(str(row[1])) for row in results))
            supplier_name_col = max(len('Supplier Name'), max(len(str(row[2])) for row in results))
            expected_date_col = max(len('Expected Date'), max(len(format_date(row[3])) for row in results))
            actual_date_col = max(len('Actual Delivery Date'), max(len(format_date(row[4])) for row in results))

            # Print the header
            header = (f"{'Delivery Name':<{delivery_name_col + 2}} {'Wine Name':<{wine_name_col + 2}} "
                      f"{'Supplier Name':<{supplier_name_col + 2}} {'Expected Date':<{expected_date_col + 2}} "
                      f"{'Actual Delivery Date':<{actual_date_col + 2}}")
            print(header)
            print('-' * len(header))

            # Print the rows
            for row in results:
                delivery_name, wine_name, supplier_name, expected_date, actual_date = row
                print(f"{delivery_name:<{delivery_name_col + 2}} {wine_name:<{wine_name_col + 2}} "
                      f"{supplier_name:<{supplier_name_col + 2}} {format_date(expected_date):<{expected_date_col + 2}} "
                      f"{format_date(actual_date):<{actual_date_col + 2}}")

    except Error as e:
        print(f"Error: '{e}' occurred while fetching the delivery data")

# Format date in MM-DD-YYYY format
def format_date(date):
    return date.strftime('%m-%d-%Y') if date else ''

# Close the cursor and the connection
def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")

def main():
    connection = create_connection()
    if connection:
        fetch_delivery_details(connection)
        close_connection(connection)

if __name__ == "__main__":
    main()