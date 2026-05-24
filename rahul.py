import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

data = pd.read_csv("automobile excel sheet.csv")
data['Observations'] = pd.to_datetime(data['Observations'], errors='coerce')
data.dropna(subset=['Observations'], inplace=True)

total_sales = data['Total sales'].sum()
most_popular_brand = data['Brand preferences'].value_counts().idxmax()
earliest_date = data['Observations'].min().date()
latest_date = data['Observations'].max().date()

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(style={'fontFamily': 'Times New Roman', 'padding': '20px', 'background': '#000000'}, children=[
    html.H1("🚗 Automobile Data Dashboard 📊", style={'textAlign': 'center', 'color': '#DAA520'}),
    html.Div(style={'display': 'flex'}, children=[
        html.Div(style={'width': '20%', 'padding': '10px', 'color': '#FFFFFF', 'background': '#1e1e1e', 'borderRadius': '10px', 'marginRight': '20px'}, children=[
            html.H3("Insights", style={'color': '#87CEEB'}),
            html.P(f"Total Sales: {total_sales} units"),
            html.P(f"Most Popular Brand: {most_popular_brand}"),
            html.P(f"Data Range: {earliest_date} to {latest_date}"),
        ]),
        html.Div(style={'width': '80%'}, children=[
            html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '20px'}, children=[
                html.Div([
                    html.Label("Select Brand:", style={'color': '#87CEEB'}),
                    dcc.Dropdown(id='brand-dropdown', options=[{'label': b, 'value': b} for b in data['Brand preferences'].unique()], multi=True, placeholder="Select a Brand", style={'width': '200px'})
                ]),
                html.Div([
                    html.Label("Select Fuel Type:", style={'color': '#87CEEB'}),
                    dcc.Dropdown(id='fuel-dropdown', options=[{'label': f, 'value': f} for f in data['Fuel types'].unique()], multi=True, placeholder="Select Fuel Type", style={'width': '200px'})
                ]),
                html.Div([
                    html.Label("Select Date Range:", style={'color': '#87CEEB'}),
                    dcc.DatePickerRange(id='date-picker-range', start_date=data['Observations'].min(), end_date=data['Observations'].max())
                ])
            ]),
            html.Div(style={'display': 'flex', 'flexWrap': 'wrap'}, children=[
                html.Div(dcc.Graph(id='line-chart'), style={'width': '48%', 'margin': '1%'}),
                html.Div(dcc.Graph(id='bar-chart'), style={'width': '48%', 'margin': '1%'}),
                html.Div(dcc.Graph(id='pie-chart'), style={'width': '48%', 'margin': '1%'}),
                html.Div(dcc.Graph(id='scatter-plot'), style={'width': '48%', 'margin': '1%'}),
                html.Div(dcc.Graph(id='box-plot'), style={'width': '48%', 'margin': '1%'}),
                html.Div(dcc.Graph(id='histogram'), style={'width': '48%', 'margin': '1%'}),
            ])
        ])
    ])
])

@app.callback(
    [Output('line-chart', 'figure'), Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure'), Output('scatter-plot', 'figure'),
     Output('box-plot', 'figure'), Output('histogram', 'figure')],
    [Input('brand-dropdown', 'value'), Input('fuel-dropdown', 'value'),
     Input('date-picker-range', 'start_date'), Input('date-picker-range', 'end_date')]
)
def update_dashboard(selected_brands, selected_fuels, start_date, end_date):
    filtered = data[(data['Observations'] >= start_date) & (data['Observations'] <= end_date)]
    if selected_brands:
        filtered = filtered[filtered['Brand preferences'].isin(selected_brands)]
    if selected_fuels:
        filtered = filtered[filtered['Fuel types'].isin(selected_fuels)]

    line = px.line(filtered, x='Observations', y='Total sales', color='Brand preferences', title="Sales Trends")
    bar = px.bar(filtered.groupby('Brand preferences')['Total sales'].sum().reset_index(), x='Brand preferences', y='Total sales', title="Brand Preferences")
    pie = px.pie(filtered, names='Fuel types', values='Total sales', title="Fuel Type Distribution")
    scatter = px.scatter(filtered, x='Observations', y='Total sales', color='Brand preferences', title="Sales by Date")
    box = px.box(filtered, x='Brand preferences', y='Total sales', title="Sales by Brand")
    hist = px.histogram(filtered, x='Total sales', title="Sales Distribution")

    return line, bar, pie, scatter, box, hist

if __name__ == '__main__':
    app.run(debug=True)