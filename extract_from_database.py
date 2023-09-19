import pandas as pd
import pyodbc

def connect_to_database(server, database, username, password):
    conn_string = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
    return pyodbc.connect(conn_string)

def retrieve_data(conn, query):
    return pd.read_sql_query(query, conn)

def main():
    server = 'localhost'
    database = 'your_database'
    username = 'your_username'
    password = 'your_password'
    queries = [
        '''
        SELECT *
        FROM table1
        ''',
        '''
        SELECT *
        FROM table2
        WHERE column = 'some_value'
        ''',
        '''
        SELECT column1, column2
        FROM table3
        '''
    ]

    # Connect to the database
    with connect_to_database(server, database, username, password) as conn:
        # Retrieve data using SQL queries
        data_frames = {}
        for query in queries:
            table_name = query.split("FROM")[1].strip()
            df = retrieve_data(conn, query)
            data_frames[table_name] = df

        # Display the retrieved data
        for table_name, df in data_frames.items():
            print(f"Table: {table_name}")
            print(df.head())
            print()

if __name__ == '__main__':
    main()
