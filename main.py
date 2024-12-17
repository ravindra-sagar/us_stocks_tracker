import os
from datetime import datetime
from python_script.fetch_and_store_data import fetch_and_store_market_data  
from python_script.query_reader import execute_query
from python_script.export_to_pdf_and_excel import export_index_to_pdf_and_excel
from python_script.dashboard import create_dashboard

def main():
    sql_scripts_path = 'sql_script'
    
    # Output PDF and Excel fill be made available in this path
    current_date = datetime.now().strftime('%Y%m%d')
    output_path = f"output_{current_date}"
    pdf_file_name = f"pdf_output_{current_date}.pdf"
    excel_file_name = f"excel_output_{current_date}.xlsx"
    
    # Name for the DuckDB database
    database_name = 'us_stocks.db'

    # Alpha Vantage API key
    api_key = 'ESQ9SU70MM8PZ9MQ'
    
    # SQL query for index creation
    index_creation_query = 'index_creation.sql'
    index_creation_query = os.path.join(sql_scripts_path, index_creation_query)
    # SQL query for getting composition
    composition_query = 'composition.sql'
    composition_query = os.path.join(sql_scripts_path, composition_query)
    # SQL query for getting additional metrics
    other_metrics_query = 'other_metrics.sql'
    other_metrics_query = os.path.join(sql_scripts_path, other_metrics_query)

    try:
        # Step 1: Upload data to DuckDB
        fetch_and_store_market_data(database_name, api_key)
        # Step 2: Querying for Index creation
        index = execute_query(database_name, index_creation_query)
        # Step 3: Exporting Index to PDF and Excel
        export_index_to_pdf_and_excel(index, output_path, excel_file_name, pdf_file_name)
        # Step 4: Creating Dashboard
        composition = execute_query(database_name, composition_query)
        other_metrics = execute_query(database_name, other_metrics_query)
        create_dashboard(index, composition, other_metrics)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()