import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Updated Working URL for IBM Dataset
URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"
data = pd.read_csv(URL)

# Initialize Dash application
app = dash.Dash(__name__)

# List of years for dropdown option
year_list = [i for i in range(1980, 2024, 1)]

# App layout
app.layout = html.Div([
    # Task 4.1: Title
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}
    ),
    
    # Task 4.2: Dropdowns
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            placeholder='Select Statistics',
            value='Select Statistics',
            style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'textAlign': 'center'}
        )
    ]),
    
    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder='Select Year',
            style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'textAlign': 'center'}
        )
    ]),
    
    # Task 4.3: Output Division
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex', 'flex-wrap': 'wrap'})
    ])
])

# Task 4.4: Disable/Enable Year Dropdown Callback
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Recession Period Statistics':
        return True
    else:
        return False

# Task 4.5 & 4.6: Render Charts Callback
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]
        
        # Plot 1: Automobile Sales fluctuation over Recession Period
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec, x='Year', y='Automobile_Sales',
                title="Average Automobile Sales Fluctuation Over Recession Period"
            )
        )

        # Plot 2: Average number of vehicles sold by vehicle type
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales, x='Vehicle_Type', y='Automobile_Sales',
                title="Average Vehicles Sold by Vehicle Type During Recessions"
            )
        )

        # Plot 3: Total advertisement expenditure share by vehicle type
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec, values='Advertising_Expenditure', names='Vehicle_Type',
                title="Total Ad Expenditure Share by Vehicle Type During Recessions"
            )
        )

        # Plot 4: Effect of unemployment rate on vehicle type and sales
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type',
                title="Effect of Unemployment Rate on Vehicle Sales by Vehicle Type"
            )
        )

        return [
            html.Div(className='chart-item', children=[R_chart1, R_chart2], style={'width': '50%'}),
            html.Div(className='chart-item', children=[R_chart3, R_chart4], style={'width': '50%'})
        ]

    elif (input_year and selected_statistics == 'Yearly Statistics'):
        yearly_data = data[data['Year'] == input_year]
        
        # Plot 1: Yearly Automobile Sales
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas, x='Year', y='Automobile_Sales',
                title="Yearly Automobile Sales Fluctuation"
            )
        )

        # Plot 2: Total Monthly Automobile Sales for selected year
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas, x='Month', y='Automobile_Sales',
                title=f"Total Monthly Automobile Sales for Year {input_year}"
            )
        )

        # Plot 3: Average vehicles sold by vehicle type for selected year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata, x='Vehicle_Type', y='Automobile_Sales',
                title=f"Average Vehicles Sold by Vehicle Type in Year {input_year}"
            )
        )

        # Plot 4: Total Advertisement Expenditure for selected year
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data, values='Advertising_Expenditure', names='Vehicle_Type',
                title=f"Total Ad Expenditure per Vehicle Type in Year {input_year}"
            )
        )

        return [
            html.Div(className='chart-item', children=[Y_chart1, Y_chart2], style={'width': '50%'}),
            html.Div(className='chart-item', children=[Y_chart3, Y_chart4], style={'width': '50%'})
        ]

    else:
        return None

if __name__ == '__main__':
    # Fixed for modern Dash versions
    app.run(debug=True)