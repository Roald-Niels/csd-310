import mysql.connector
from mysql.connector import Error
import select

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
       
def show_film(cursor, title):

    cursor.execute("select film_name as Name. film_director, genre_name as Genre, studio_name as ‘Studio Name’ from film INNER JOIN genre ON film.genre_id””genre.genre_id INNER JOIN studio ON film.studio_id””studio.studio_id")
    films = cursor.fetchall()
    print("\n – {} –".format(title))
    for film in films:
        print("film Name: {} \nDirector: {}\nGenre Name ID: {}\nStudio Name: {}\n".format(film[0], film[1], film[2], film[3]))

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
        
        fetch_and_print_results(
            conn, "SELECT film_name as Name, film_director as Director, genre_name as Genre, studio_name as 'Studio Name' from film INNER JOIN genre ON film.genre_id=genre.genre_id INNER JOIN studio ON film.studio_id=studio.studio_id","DISPLAYING FILMS")
                
        # Create a cursor
        cursor = conn.cursor()
        # Create table
        cursor.execute("INSERT INTO film VALUES('Dungeons & Dragons: Honor Among Thieves',', '2023', '124', 'John Francis Daley')")
        print("Inserted",cursor.rowcount,"row(s) of data. ")
        # Commit changes and close connection
        conn.commit()
        cursor.close()
        
        fetch_and_print_results(
            conn, "SELECT film_name as Name, film_director as Director, genre_name as Genre, studio_name as 'Studio Name' from film INNER JOIN genre ON film.genre_id=genre.genre_id INNER JOIN studio ON film.studio_id=studio.studio_id","DISPLAYING FILMS AFTER INSERT")

        mycursor = conn.cursor()

        sql = "UPDATE film SET = 'Alien' WHERE genre = 'horror'"

        mycursor.execute(sql)
        conn.commit()
        fetch_and_print_results(
            conn, "SELECT film_name as Name, film_director as Director, genre_name as Genre, studio_name as 'Studio Name' from film INNER JOIN genre ON film.genre_id=genre.genre_id INNER JOIN studio ON film.studio_id=studio.studio_id","DISPLAYING FILMS AFTER UPDATE")
        mycursor = conn.cursor()

        sql = "DELETE FROM film WHERE film_name = 'Gladiator'"

        mycursor.execute(sql)

        fetch_and_print_results(
            conn, "SELECT film_name as Name, film_director as Director, genre_name as Genre, studio_name as 'Studio Name' from film INNER JOIN genre ON film.genre_id=genre.genre_id INNER JOIN studio ON film.studio_id=studio.studio_id","DISPLAYING FILMS AFTER DELETE")

        conn.commit()

    conn.close()

if __name__ == "__main__":
    main()

    
