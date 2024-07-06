import mysql.connector
from mysql.connector import Error

def connect():
    """ Connect to MySQL database """
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            database='movies',  
            user='root',  
            password='Blackops19!'
        )
        if conn.is_connected():
            print('Connected to MySQL database')
            return conn
    except Error as e:
        print(e)

def fetch_and_print_results(conn, query, description):
    """ Fetch the results for a given query and print them """
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        print(description)
        for row in result:
            print(row)
        print("\n")
    except Error as e:
        print(f"Error: '{e}'")

def main():
    # Step 1: Connect to the database
    conn = connect()

    if conn:
        # Step 2: Query 1 - Select all fields from the studio table
        fetch_and_print_results(conn, "SELECT * FROM studio",
                                "Query 1: All fields for the studio table")

        # Step 3: Query 2 - Select all fields from the genre table
        fetch_and_print_results(conn, "SELECT * FROM genre",
                                "Query 2: All fields for the genre table")

        # Step 4: Query 3 - Select movie names with runtime less than two hours
        fetch_and_print_results(
            conn, "SELECT film_name, film_runtime FROM film WHERE film_runtime < 120",
            "Query 3: Movie names with runtime less than two hours")
           

           # Step 5: Query 4 - Select film names and directors grouped by director
        fetch_and_print_results(
            conn, "SELECT film_director, film_name FROM film",
            "Query 4: Film names and directors grouped by director")

        # Close the connection
        conn.close()

if __name__ == "__main__":
    main()