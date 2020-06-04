
import sqlite3


def create_table():
    """
    Start a connection to the database
    Create a table if it does not exist
    Close the connection
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS people (
                    ID INTEGER UNIQUE, 
                    name TEXT, 
                    city TEXT, 
                    country TEXT, 
                    email TEXT, 
                    tel TEXT);
                    """)

    conn.commit()
    conn.close()


def add(id_value, name_value, city_value, country_value, email_value, tel_value):
    """
    Start a connection to the database
    Insert a user if he is not in the table
    Close the connection
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTO  people VALUES (?, ?, ?, ?, ?, ?)",
                   (id_value, name_value, city_value, country_value, email_value, tel_value))

    conn.commit()
    conn.close()


def delete(id_user):
    """
    Start a connection to the database
    Delete a user using the ID
    Close the connection
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM people WHERE ID = (?)", id_user)

    conn.commit()
    conn.close()


def delete_all():
    """
    Start a connection to the database
    Delete all users from the table
    Close the connection
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM people")

    conn.commit()
    conn.close()


def check(id_user):
    """
    Start a connection to the database
    Select a certain user using the ID, and returning the personal data
    Close the connection
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM people WHERE ID = (?)", id_user)
    result = cursor.fetchone()

    conn.commit()
    conn.close()

    return result
