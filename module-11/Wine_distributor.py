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

def show_distributor_wine_relationships(connection):
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        
        query = """
        SELECT DISTINCT 
            d.distributor_id, 
            d.distributor_name, 
            w.wine_id, 
            w.wine_name
        FROM 
            distributor d
        JOIN 
            delivery del ON d.distributor_id = del.distributor_id
        JOIN 
            orders o ON del.delivery_id = o.delivery_id
        JOIN 
            wine w ON o.wine_id = w.wine_id
        ORDER BY 
            d.distributor_id, w.wine_id
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        if not results:
            print("No distributor-wine relationships found.")
        else:
            print("\nDistributors and the wines they carry:")
            print("-" * 50)
            current_distributor = None
            for row in results:
                if current_distributor != row['distributor_id']:
                    if current_distributor is not None:
                        print()  # Add a blank line between distributors
                    print(f"Distributor: {row['distributor_name']} (ID: {row['distributor_id']})")
                    current_distributor = row['distributor_id']
                print(f"  - {row['wine_name']} (Wine ID: {row['wine_id']})")
            
    except Error as e:
        print(f"Error: '{e}' occurred")
    finally:
        if cursor:
            cursor.close()

def main():
    connection = create_connection()
    if connection is not None:
        try:
            show_distributor_wine_relationships(connection)
        finally:
            connection.close()
            print("\nMySQL connection is closed")

if __name__ == "__main__":
    main()