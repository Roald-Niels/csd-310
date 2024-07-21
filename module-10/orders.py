import mysql.connector
from mysql.connector import Error

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

def fetch_orders_deliveries(connection):
    try:
        cursor = connection.cursor()
        query = """
        SELECT o.order_date, o.orders_id, o.inventory_id, o.supplier_id, o.delivery_id, o.wine_id,
               d.delivery_name, DATE_FORMAT(d.expected_date, '%M %d, %Y') AS expected_date,
               DATE_FORMAT(d.actual_date, '%M %d, %Y') AS actual_date
        FROM orders o
        JOIN deliveries d ON o.delivery_id = d.delivery_id;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            print("No data found.")
        else:
            # Calculate column widths dynamically
            columns = [
                ('Order Date', lambda row: len(str(row[0]))),
                ('Order ID', lambda row: len(str(row[1]))),
                ('Inventory ID', lambda row: len(str(row[2]))),
                ('Supplier ID', lambda row: len(str(row[3]))),
                ('Delivery ID', lambda row: len(str(row[4]))),
                ('Wine ID', lambda row: len(str(row[5]))),
                ('Delivery Name', lambda row: len(str(row[6]))),
                ('Expected Date', lambda row: len(str(row[7]))),
                ('Actual Date', lambda row: len(str(row[8])))
            ]
            widths = [max(len(name), max(calc(row) for row in results)) + 2 for name, calc in columns]

            # Print the header
            header = "".join([f"{name:<{width}}" for name, width in zip([col[0] for col in columns], widths)])
            print(header)
            print('-' * sum(widths))

            # Print the rows
            for row in results:
                print("".join([f"{str(col):<{width}}" for col, width in zip(row, widths)]))

    except Error as e:
        print(f"Error: '{e}' occurred while fetching the data")

def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")

def main():
    connection = create_connection()
    if connection:
        fetch_orders_deliveries(connection)
        close_connection(connection)

if __name__ == "__main__":
    main()