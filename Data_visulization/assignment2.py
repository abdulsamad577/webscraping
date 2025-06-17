import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load dataset (Replace with actual file path if using CSV)
data = pd.read_csv("histo.csv")  # Ensure the correct file path

dashboard_app = dash.Dash(__name__)

year_list = [i for i in range(1980, 2024, 1)]

dashboard_app.layout = html.Div([
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': '24px'}
    ),
    
    # Dropdown for selecting report type
    html.Div([
        html.Label("Select Report Type:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            placeholder='Select a report type',
            value='Yearly Statistics',
            style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'textAlign': 'center'}
        )
    ], style={'width': '50%', 'margin': 'auto'}),
    
    # Dropdown for selecting year
    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': str(year), 'value': year} for year in year_list],
            placeholder='Select a year',
            value=1980,
            disabled=False,
            style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'textAlign': 'center'}
        )
    ], style={'width': '50%', 'margin': 'auto'}),
    
    # Output container
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex', 'flex-wrap': 'wrap'})
    ])
])

# Callback to enable/disable year dropdown
@dashboard_app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_input_container(report_type):
    return report_type == 'Recession Period Statistics'

# Callback to update the output container
@dashboard_app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'), Input('select-year', 'value')]
)
def update_output_container(report_type, year):
    if report_type == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]
        
        # Plot 1: Automobile sales fluctuate over Recession Period (year wise)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, x='Year', y='Automobile_Sales', title="Automobile Sales over Recession Period")
        )

        # Plot 2: Average number of vehicles sold by vehicle type
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales', title="Average Vehicle Sales by Type")
        )
        
        # Plot 3: Pie chart for total expenditure share by vehicle type
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type', title="Advertising Expenditure by Vehicle Type")
        )
        
        # Plot 4: Effect of unemployment rate on vehicle type and sales
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_data, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type',
                          labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
                          title='Effect of Unemployment Rate on Vehicle Type and Sales')
        )

        return [
            html.Div(children=[R_chart1, R_chart2], style={'display': 'flex', 'width': '100%'}),
            html.Div(children=[R_chart3, R_chart4], style={'display': 'flex', 'width': '100%'})
        ]
    
    else:  # Yearly Statistics
        yearly_data = data[data['Year'] == year]
        
        # Plot 1: Automobile Sales per Month
        monthly_sales = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(monthly_sales, x='Month', y='Automobile_Sales', title="Monthly Automobile Sales in Selected Year")
        )
        
        # Plot 2: Consumer confidence over the year
        conf_data = yearly_data.groupby('Month')['Consumer_Confidence'].mean().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(conf_data, x='Month', y='Consumer_Confidence', title="Consumer Confidence Throughout the Year")
        )
        
        # Plot 3: Advertising expenditure trend
        adv_exp = yearly_data.groupby('Month')['Advertising_Expenditure'].sum().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(adv_exp, x='Month', y='Advertising_Expenditure', title="Monthly Advertising Expenditure")
        )
        
        # Plot 4: Automobile Sales by Vehicle Type
        sales_by_type = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(sales_by_type, values='Automobile_Sales', names='Vehicle_Type', title="Sales Distribution by Vehicle Type")
        )

        return [
            html.Div(children=[Y_chart1, Y_chart2], style={'display': 'flex', 'width': '100%'}),
            html.Div(children=[Y_chart3, Y_chart4], style={'display': 'flex', 'width': '100%'})
        ]

if __name__ == '__main__':
    dashboard_app.run(debug=True)