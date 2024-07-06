import psycopg2
import os

# Database connection parameters
DB_NAME = 'trivialCompute'  # Case-sensitive name
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'

# Directory containing SQL scripts to execute
SQL_SCRIPTS_DIR = './scripts'

def connect():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(dbname='postgres', user=DB_USER, password=DB_PASSWORD, host='localhost')
        conn.autocommit = True
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

def drop_create_database(conn):
    try:
        # Create a cursor object
        cur = conn.cursor()

        # Force drop the database if it exists (case-insensitive)
        cur.execute(f"SELECT pg_terminate_backend(pg_stat_activity.pid) "
                    f"FROM pg_stat_activity "
                    f"WHERE pg_stat_activity.datname = '{DB_NAME}' "
                    f"AND pid <> pg_backend_pid();")
        cur.execute(f"DROP DATABASE IF EXISTS \"{DB_NAME}\"")

        # Create the database with the exact case-sensitive name
        cur.execute(f"CREATE DATABASE \"{DB_NAME}\"")

        # Close the cursor and commit the transaction
        cur.close()
        conn.commit()

        print(f"Database '{DB_NAME}' created successfully.")

    except psycopg2.Error as e:
        print(f"Error creating database: {e}")

def execute_sql_scripts(conn):
    try:
        # Create a cursor object
        cur = conn.cursor()

        # List all .sql files in the directory
        sql_files = [file for file in os.listdir(SQL_SCRIPTS_DIR) if file.endswith('.sql')]

        # Execute each SQL script
        for file in sql_files:
            script_path = os.path.join(SQL_SCRIPTS_DIR, file)
            with open(script_path, 'r') as f:
                sql_script = f.read()
                cur.execute(sql_script)
                print(f"Executed script '{file}'")

        # Close the cursor and commit the transaction
        cur.close()
        conn.commit()

        print("All SQL scripts executed successfully.")

    except psycopg2.Error as e:
        print(f"Error executing SQL scripts: {e}")

def setup_database_and_execute_scripts():
    # Connect to PostgreSQL
    conn = connect()
    if conn is None:
        return

    try:
        # Drop and create the database
        drop_create_database(conn)

        # Connect to the newly created database
        conn.close()
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host='localhost')

        # Execute SQL scripts in the database
        execute_sql_scripts(conn)

        print("Database setup and SQL script execution completed.")

    finally:
        # Close the connection
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    setup_database_and_execute_scripts()
