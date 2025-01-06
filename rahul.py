import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
data = pd.read_csv("automobile excel sheet.csv")
data['Observations'] = pd.to_datetime(data['Observations'], errors='coerce')
data.dropna(subset=['Observations'], inplace=True)

# Generate some insights based on the data
total_sales = data['Total sales'].sum()
most_popular_brand = data['Brand preferences'].value_counts().idxmax()
earliest_date = data['Observations'].min().date()
latest_date = data['Observations'].max().date()

# Initialize Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div(style={'fontFamily': 'Times New Roman', 'padding': '20px', 'background': '#000000', 'height': '100vh'}, children=[
    html.H1("🚗 Automobile Data Dashboard 📊", style={'textAlign': 'center', 'color': '#DAA520', 'background': '#000', 'padding': '10px', 'borderRadius': '10px'}),
    html.Div(style={'display': 'flex', 'flexDirection': 'row'}, children=[
        html.Div(style={'width': '20%', 'padding': '10px', 'color': '#FFFFFF', 'background': '#1e1e1e', 'borderRadius': '10px', 'marginRight': '20px', 'overflowY': 'scroll'}, children=[
            html.H3("Automobile Sales Insights", style={'color': '#87CEEB'}),
            html.P(f"Total Sales (1976-2024): {total_sales} units"),
            html.P(f"Most Popular Brand: {most_popular_brand}"),
            html.P(f"Data Range: {earliest_date} to {latest_date}"),
            html.H3("Brands and Models", style={'color': '#87CEEB'}),
            html.P("The file features a wide range of automobile brands such as Toyota, Suzuki, Tata Motors, Mahindra, Hyundai, Nissan, Xiaomi, Tesla, BYD, and Kia Corporation. Models include various trims and body types like sedans, SUVs, coupes, convertibles, hatchbacks, minivans, and wagons."),
            html.H3("Fuel Types", style={'color': '#87CEEB'}),
            html.P("Vehicles use different fuel types: gasoline, ethanol, diesel, bio-diesel, and hybrid options. Gasoline and ethanol are the most common, with a significant presence of diesel and bio-diesel vehicles, indicating a trend towards diverse fuel options."),
            html.H3("Transmission", style={'color': '#87CEEB'}),
            html.P("The majority of vehicles have automatic transmissions, with a few manual options, reflecting a preference for automatic vehicles over the years."),
            html.H3("Trends and Insights", style={'color': '#87CEEB'}),
            html.P("Toyota and Suzuki are frequently mentioned, suggesting they are popular brands in the file. Other brands like Mahindra, Hyundai, and Nissan also have significant entries, indicating their market presence."),
            html.P("The file shows a variety of fuel types, with a noticeable shift towards more environmentally friendly options like ethanol and hybrid vehicles."),
            html.P("Sedans and SUVs are the most common body types, with a wide range of trims, indicating diverse consumer preferences."),
            html.P("Automatic transmissions dominate the file, highlighting a long-term trend towards automatic vehicles.")
        ]),
        html.Div(style={'width': '80%'}, children=[
            html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'marginBottom': '20px'}, children=[
                html.Div(children=[
                    html.Label("Select Brand:", style={'fontWeight': 'bold', 'color': '#87CEEB'}),
                    dcc.Dropdown(id='brand-dropdown', options=[{'label': brand, 'value': brand} for brand in data['Brand preferences'].unique()], multi=True, placeholder="Select a Brand", style={'width': '200px'})
                ]),
                html.Div(children=[
                    html.Label("Select Fuel Type:", style={'fontWeight': 'bold', 'color': '#87CEEB'}),
                    dcc.Dropdown(id='fuel-dropdown', options=[{'label': fuel, 'value': fuel} for fuel in data['Fuel types'].unique()], multi=True, placeholder="Select a Fuel Type", style={'width': '200px'})
                ]),
                html.Div(children=[
                    html.Label("Select Date Range:", style={'fontWeight': 'bold', 'color': '#87CEEB'}),
                    dcc.DatePickerRange(id='date-picker-range', start_date=data['Observations'].min(), end_date=data['Observations'].max())
                ])
            ]),
            html.Div(style={'display': 'flex', 'flexWrap': 'wrap'}, children=[
                html.Div(dcc.Graph(id='line-chart'), style={'width': '48%', 'margin': '1%', 'background': '#1e1e1e'}),
                html.Div(dcc.Graph(id='bar-chart'), style={'width': '48%', 'margin': '1%', 'background': '#1e1e1e'}),
                html.Div(dcc.Graph(id='pie-chart'), style={'width': '48%', 'margin': '1%', 'background': '#1e1e1e'}),
                html.Div(dcc.Graph(id='scatter-plot'), style={'width': '48%', 'margin': '1%', 'background': '#1e1e1e'}),
                html.Div(dcc.Graph(id='box-plot'), style={'width': '48%', 'margin': '1%', 'background': '#1e1e1e'}),
                html.Div(dcc.Graph(id='histogram'), style={'width': '48%', 'margin': '1%', 'background': '#1e1e1e'}),
            ]),
            html.Div(id='summary-table', style={'marginTop': '20px', 'padding': '10px', 'background': '#fff'})
        ])
    ])
])

# Callback to update charts based on user input
@app.callback(
    [Output('line-chart', 'figure'),
     Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure'),
     Output('scatter-plot', 'figure'),
     Output('box-plot', 'figure'),
     Output('histogram', 'figure'),
     Output('summary-table', 'children')],
    [Input('brand-dropdown', 'value'),
     Input('fuel-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_dashboard(selected_brands, selected_fuel_types, start_date, end_date):
    filtered_data = data[(data['Observations'] >= start_date) & (data['Observations'] <= end_date)]
    if selected_brands:
        filtered_data = filtered_data[filtered_data['Brand preferences'].isin(selected_brands)]
    if selected_fuel_types:
        filtered_data = filtered_data[filtered_data['Fuel types'].isin(selected_fuel_types)]

    line_chart = px.line(filtered_data, x='Observations', y='Total sales', color='Brand preferences', title="Sales Trends", labels={'Observations': 'Date', 'Total sales': 'Sales'})
    line_chart.update_layout(plot_bgcolor='#E0FFFF', paper_bgcolor='#E0FFFF')

    bar_chart_data = filtered_data.groupby('Brand preferences')['Total sales'].sum().reset_index()
    bar_chart = px.bar(bar_chart_data, x='Brand preferences', y='Total sales', color='Brand preferences', title="Brand Preferences", labels={'Brand preferences': 'Brand', 'Total sales': 'Sales'})
    bar_chart.update_layout(plot_bgcolor='#F5F5DC', paper_bgcolor='#F5F5DC')

    pie_chart = px.pie(filtered_data, names='Fuel types', values='Total sales', title="Fuel Type Distribution")
    pie_chart.update_layout(plot_bgcolor='#FFEFD5', paper_bgcolor='#FFEFD5')

    scatter_plot = px.scatter(filtered_data, x='Observations', y='Total sales', color='Brand preferences', title="Sales by Date")
    scatter_plot.update_layout(plot_bgcolor='#FFFACD', paper_bgcolor='#FFFACD')

    box_plot = px.box(filtered_data, x='Brand preferences', y='Total sales', title="Box Plot of Sales by Brand", labels={'Brand preferences': 'Brand', 'Total sales': 'Sales'})
    box_plot.update_layout(plot_bgcolor='#FFEBEE', paper_bgcolor='#FFEBEE')

    histogram = px.histogram(filtered_data, x='Total sales', title="Sales Distribution", labels={'Total sales': 'Sales'})
    histogram.update_layout(plot_bgcolor='#FFFACD', paper_bgcolor='#FFFACD')

    summary = filtered_data.groupby('Brand preferences')['Total sales'].sum().reset_index()
    summary_table = html.Table([
        html.Thead(html.Tr([html.Th(col) for col in summary.columns])),
        html.Tbody([html.Tr([html.Td(summary.iloc[i][col]) for col in summary.columns]) for i in range(len(summary))])
    ])

    return line_chart, bar_chart, pie_chart, scatter_plot, box_plot, histogram, summary_table

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
