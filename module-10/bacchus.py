import mysql.connector
from mysql.connector import Error

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

# Fetch and print customers' order deliveries
def fetch_customers_order_deliveries(connection):
    try:
        cursor = connection.cursor()
        query = """
        SELECT deliveries.delivery_name, wine.wine_type, supplier.supplier_name
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

            # Print the header
            header = f"{'Delivery Name':<{delivery_name_col + 2}} {'Wine Name':<{wine_name_col + 2}} {'Supplier Name':<{supplier_name_col + 2}}"
            print(header)
            print('-' * len(header))

            # Print the rows
            for row in results:
                delivery_name, wine_name, supplier_name = row
                print(f"{delivery_name:<{delivery_name_col + 2}} {wine_name:<{wine_name_col + 2}} {supplier_name:<{supplier_name_col + 2}}")

    except Error as e:
        print(f"Error: '{e}' occurred while fetching the delivery data")

# Close the cursor and the connection
def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")

def main():
    connection = create_connection()
    if connection:
        fetch_customers_order_deliveries(connection)
        close_connection(connection)

if __name__ == "__main__":
    main()