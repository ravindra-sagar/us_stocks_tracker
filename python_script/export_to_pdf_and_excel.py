import os
import pandas as pd
from fpdf import FPDF



# Custom function to add headers
def add_headers(pdf, index, column_widths):
    pdf.set_fill_color(173, 216, 230)  # Light Blue for headers
    for i, col in enumerate(index.columns):
        pdf.cell(column_widths[i], 10, col, border=1, align='C', fill=True)
    pdf.ln()

def export_index_to_pdf_and_excel(index, output_path, excel_file_name, pdf_file_name):
    # Creating a copy, so that original data frame remains unchanged with downstream operations
    index = index.copy()

    # Check if the directory exists, if not, create it
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Generate the full output file path
    output_excel_path = os.path.join(output_path, excel_file_name)

    # If the file exists, delete it
    if os.path.exists(output_excel_path):
        os.remove(output_excel_path)

    # Formatting Index
    index['Date'] = index['Date'].dt.date
    index['Adjusted Close (USD)'] = index['Adjusted Close']
    index['Market Capitalization (USD)'] = index['Market Capitalization']

    # Exporting to Excel File
    index[['Date', 'Adjusted Close (USD)', 'Outstanding Shares', 'Market Capitalization (USD)']].to_excel(output_excel_path, index=False)
    print(f"Excel saved to {output_excel_path}")

    # Generate the full output file path
    output_pdf_path = os.path.join(output_path, pdf_file_name)
    
    # If the file exists, delete it
    if os.path.exists(output_pdf_path):
        os.remove(output_pdf_path)

    # Formatting Index
    index['Adjusted Close (USD)'] = index['Adjusted Close'].round(2)
    index['Outstanding Shares (In Million)'] = index['Outstanding Shares']/1000000
    index['Outstanding Shares (In Million)'] = index['Outstanding Shares (In Million)'].round(2)
    index['Market Capitalization (In Billion USD)'] = index['Market Capitalization']/1000000000
    index['Market Capitalization (In Billion USD)'] = index['Market Capitalization (In Billion USD)'].round(2)
    index = index[['Date', 'Adjusted Close (USD)', 'Outstanding Shares (In Million)', 'Market Capitalization (In Billion USD)']]

    # Create PDF instance
    pdf = FPDF(orientation='L', unit='mm', format='A4')  
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()

    # Adjust font size based on column count
    page_width = 297 - 20  # A4 width (297mm) minus left & right margins (10mm each)
    page_height = 210 - 20 # A4 height (210mm) minus top & bottom margins (10mm each)
    column_count = len(index.columns)
    max_column_width = page_width / column_count
    font_size = min(10, max(6, max_column_width / 2))  # Dynamically adjust font size
    pdf.set_font("Arial", size=font_size)

    # Calculate column widths based on content
    column_widths = []
    for col in index.columns:
        max_content_length = max(index[col].astype(str).apply(len).max(), len(col))
        column_width = max_content_length * 2.5  # Adjust multiplier for font size
        column_widths.append(column_width)

    # Ensure total width fits within the page
    total_width = sum(column_widths)
    if total_width > page_width:
        scale_factor = page_width / total_width
        column_widths = [w * scale_factor for w in column_widths]


    # Add header for the first page
    add_headers(pdf, index, column_widths)

    # Add rows dynamically
    for row_index, row in index.iterrows():
        if pdf.get_y() > 190:  # Check if space on the page is running out (A4 height is 210mm)
            pdf.add_page()
            add_headers(pdf, index, column_widths)  # Add headers on the new page

        for i, col in enumerate(index.columns):
            cell_value = str(row[col])
            if col in ['Date']:
                pdf.set_fill_color(211, 211, 211)  # Light Grey for Date and Ticker
                pdf.cell(column_widths[i], 10, cell_value, border=1, align='C', fill=True)
            else:
                pdf.cell(column_widths[i], 10, cell_value, border=1, align='C')
        pdf.ln()


    # Save PDF to the specified path
    pdf.output(output_pdf_path)
    print(f"PDF saved to {output_pdf_path}")
