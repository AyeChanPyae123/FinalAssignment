import sqlite3
import pandas as pd

# City population data
POPULATION = {
    "London": 8982000,
    "New York": 8419000,
    "Tokyo": 37400068,
    "Delhi": 31181376,
    "Paris": 2148000
}

# Load weather data
conn = sqlite3.connect("weather_data.db")
df = pd.read_sql("SELECT * FROM weather", conn)

# Add population data
df["population"] = df["city"].map(POPULATION)

# Save enriched data
df.to_sql("weather_enriched", conn, if_exists="replace", index=False)
conn.close()
print("Enriched data saved to SQLite database.")