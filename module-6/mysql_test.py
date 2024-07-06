import mysql.connector
from mysql.connector import errorcode

config = {
    "user": "root", "password": "Blackops19!", "host": "127.0.0.1",
    "database": "movies", "raise_on_warnings": True
}

db = None

try:
    db = mysql.connector.connect(**config)
    print("\n Database user {} connected to mysql on host {} with database {}".format(config["user"], config["host"], config["database"]))
    input("\n\n Press any key to continue...")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist")
    else:
        print(err)
finally:
    if db is not None:
        db.close()

def main():

    if conn:
        # Step 2: Query 1 - Select all fields from the studio table
        fetch_and_print_results(conn, "SELECT * FROM studio",
                                "Query 1: All fields for the studio table")

        # Step 3: Query 2 - Select all fields from the genre table
        fetch_and_print_results(conn, "SELECT * FROM genre",
                                "Query 2: All fields for the genre table")

        # Step 4: Query 3 - Select movie names with runtime less than two hours
        fetch_and_print_results(
            conn, "SELECT name, runtime FROM movies WHERE runtime < 120",
            "Query 3: Movie names with runtime less than two hours")

        # Step 5: Query 4 - Select film names and directors grouped by director
        fetch_and_print_results(
            conn, "SELECT director, name FROM films GROUP BY director",
            "Query 4: Film names and directors grouped by director")

        # Close the connection
        conn.close()

if __name__ == "__main__":
    main()