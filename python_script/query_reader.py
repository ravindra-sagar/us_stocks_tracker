import duckdb
import pandas as pd

def execute_query (db_file, sql_file):
    # Connect to the DuckDB database
    conn = duckdb.connect(db_file)
    # Reading SQL query
    with open(sql_file, "r") as file:
        sql_query = file.read()
    # Execute the SQL query and fetch the results into a DataFrame
    index = conn.execute(sql_query).fetchdf()
    # Close the connection
    conn.close()
    # Final Output
    return index