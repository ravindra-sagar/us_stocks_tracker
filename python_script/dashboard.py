import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

def create_dashboard(index, composition, other_metrics):
    # Initialize the Dash app
    app = dash.Dash(__name__)

    # Layout for the app
    app.layout = html.Div([
        html.H2("Index Performance", style={
            'textAlign': 'center',
            'fontFamily': 'Arial, sans-serif',  # Set font for title
            'fontSize': '32px'  # Consistent font size for main title
        }),
        
        # First graph: Line chart
        html.Div([
            dcc.Graph(
                id='line-chart',
                figure=px.line(
                    index,
                    x='Date',
                    y='Adjusted Close',
                    labels={'Date': 'Date (Last 30 Days)', 'Adjusted Close': 'Price (USD)'},
                    template='plotly_white'
                ).update_layout(
                    xaxis=dict(
                        showline=True,
                        linewidth=1,
                        linecolor='black',
                        mirror=True,
                        tickformat='%b-%d-%Y'  # MMM-DD-YYYY format
                    ),
                    yaxis=dict(
                        showline=True,
                        linewidth=1,
                        linecolor='black',
                        mirror=True
                    )
                )
            )
        ], style={'marginBottom': '50px'}),
        
        # Dropdown and second view: Index Composition Table
        html.Div([
            html.H2("Index Composition", style={
                'textAlign': 'center',
                'marginBottom': '50px',  # Increased space after title
                'fontFamily': 'Arial, sans-serif',  # Set font for table title
                'fontSize': '32px'  # Consistent font size for second title
            }),
            html.Label("Select a Date:", style={
                'fontWeight': 'bold',
                'fontFamily': 'Arial, sans-serif',  # Set font for the label
                'fontSize': '16px'  # Font size for the label
            }),
            dcc.Dropdown(
                id='date-dropdown',
                options=[
                    {'label': date.strftime('%b-%d-%Y'), 'value': date}
                    for date in sorted(composition['Date'].unique())
                ],
                value=composition['Date'].min(),  # Default to the first available date
                placeholder="Select a date",
                style={'width': '50%', 'fontFamily': 'Arial, sans-serif', 'fontSize': '16px'}  # Set font for dropdown
            ),
            dash_table.DataTable(
                id='composition-table',
                style_cell={
                    'textAlign': 'center',  # Align values to center
                    'fontFamily': 'Arial, sans-serif',  # Set font for table cells
                    'fontSize': '14px'  # Font size for table content
                },
                style_header={
                    'textAlign': 'center', 
                    'fontWeight': 'bold',
                    'fontFamily': 'Arial, sans-serif',  # Set font for table header
                    'fontSize': '16px'  # Font size for table header
                }
            )
        ], style={'marginBottom': '50px'}),

        # Third view: Other Metrics Table (Static Display)
        html.Div([
            html.H2("Other Metrics", style={
                'textAlign': 'center',
                'marginBottom': '50px',  # Space after title
                'fontFamily': 'Arial, sans-serif',  # Set font for table title
                'fontSize': '32px'  # Consistent font size for third title
            }),
            dash_table.DataTable(
                id='other-metrics-table',
                style_cell={
                    'textAlign': 'center',  # Align values to center
                    'fontFamily': 'Arial, sans-serif',  # Set font for table cells
                    'fontSize': '14px'  # Font size for table content
                },
                style_header={
                    'textAlign': 'center', 
                    'fontWeight': 'bold',
                    'fontFamily': 'Arial, sans-serif',  # Set font for table header
                    'fontSize': '16px'  # Font size for table header
                },
                # Use the entire DataFrame for static display
                columns=[
                    {'name': 'Date', 'id': 'Date'},
                    {'name': 'Change in Composition', 'id': 'Change in Composition'},
                    {'name': 'No of Changes in Composition', 'id': 'No of Changes in Composition'},
                    {'name': 'Cumulative Return %', 'id': 'Cumulative Return %'},
                    {'name': 'Daily Return %', 'id': 'Daily Return %'}
                ],
                data=other_metrics.to_dict('records')  # Display all data without filtering by date
            )
        ])
    ])

    # Callback to update the "Index Composition" table based on selected date
    @app.callback(
        Output('composition-table', 'data'),
        Output('composition-table', 'columns'),
        [Input('date-dropdown', 'value')]
    )
    def update_composition_table(selected_date):
        if selected_date is None:
            return [], []  # Return empty table if no date is selected

        # Filter the composition DataFrame for the selected date
        filtered_data = composition[composition['Date'] == selected_date]

        # Define the columns for the DataTable
        columns = [
            {'name': 'Ticker', 'id': 'Ticker'},
            {'name': 'Company', 'id': 'Company'},
            {'name': 'Exchange', 'id': 'Exchange'},
            {'name': 'Adjusted Close (In USD)', 'id': 'Adjusted Close (In USD)'},
            {'name': 'Outstanding Shares (In Million)', 'id': 'Outstanding Shares (In Million)'},
            {'name': 'Market Capitalization (In Billion USD)', 'id': 'Market Capitalization (In Billion USD)'}
        ]
        
        # Convert the DataFrame to a list of dictionaries for the DataTable
        data = filtered_data.to_dict('records')

        return data, columns

    # Start the server and open the browser automatically
    app.run_server(debug=True, use_reloader=False)

