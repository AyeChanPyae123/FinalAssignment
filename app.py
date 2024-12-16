import dash
from dash import dcc, html, Input, Output
import pandas as pd
import sqlite3
import plotly.express as px

# Load data
conn = sqlite3.connect("weather_data.db")
df = pd.read_sql("SELECT * FROM weather_enriched", conn)
conn.close()

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Weather Dashboard", style={"textAlign": "center"}),
    dcc.Dropdown(
        id="city-dropdown",
        options=[{"label": city, "value": city} for city in df["city"]],
        value=df["city"].iloc[0]
    ),
    dcc.Graph(id="weather-graph"),
    html.Div(id="city-info", style={"textAlign": "center", "marginTop": "20px"})
])

@app.callback(
    [Output("weather-graph", "figure"), Output("city-info", "children")],
    [Input("city-dropdown", "value")]
)
def update_dashboard(selected_city):
    city_data = df[df["city"] == selected_city]
    fig = px.bar(
        x=["temperature", "humidity", "wind_speed"],
        y=[city_data["temperature"].iloc[0], city_data["humidity"].iloc[0], city_data["wind_speed"].iloc[0]],
        labels={"x": "Metrics", "y": "Value"},
        title=f"Weather Metrics for {selected_city}"
    )
    info = f"{selected_city} has a population of {city_data['population'].iloc[0]:,} people. Current weather: {city_data['weather'].iloc[0]}."
    return fig, info

if __name__ == "__main__":
    app.run_server(debug=True)
