import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Daten aus CSV-Datei lesen
df = pd.read_csv('/Users/patrickfunke/CodeHub/Projectautos/data/cleaned_electric_cars_data_final.csv')

# Mapbox Token setzen
token = 'YOUR_MAPBOX_TOKEN'

# Farbpalette für die Skala von blau nach grün
color_scale = np.linspace(0, 1, 10)  # 10 Stufen von blau nach grün
colors = [f'rgb(0, 0, {int(255 * c)})' for c in color_scale]  # RGB-Farbwerte erzeugen

# Karte erstellen
fig = go.Figure()

# Städte hinzufügen
for city in df['City'].unique():
    city_data = df[df['City'] == city]
    city_vehicle_count = city_data['Model'].nunique()  # Anzahl der einzigartigen Fahrzeugmodelle in der Stadt
    if city_vehicle_count > 0:
        size = np.log(city_vehicle_count + 1) * 2  # Logarithmische Skalierung der Kreisgröße
    else:
        size = 3  # Mindestgröße für Städte ohne Fahrzeuge
    # Farbe basierend auf der Anzahl der Fahrzeuge festlegen
    color_index = min(int(city_vehicle_count / (df['Model'].nunique() / len(colors))), len(colors) - 1)
    color = colors[color_index]
    fig.add_trace(go.Scattermapbox(
        lat=[city_data.iloc[0]['breitengrad']],  # Breitengrad der Stadt
        lon=[city_data.iloc[0]['laengengrad']],  # Längengrad der Stadt
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=size,  # Kreisgröße basierend auf logarithmisch transformierten Anzahl der einzigartigen Fahrzeuge
            color=color,  # Farbe der Marker basierend auf der Skala
            opacity=0.3, # Transparenz der Marker
            showscale=True,
        ),
        hoverinfo='text',
        hovertext=f"City: {city}<br>Total Vehicles: {city_vehicle_count}",
        name=city
    ))

# Layout der Karte einstellen
fig.update_layout(
    mapbox=dict(
        accesstoken='pk.eyJ1Ijoid2kyMzA0NCIsImEiOiJjbHUzNnhkN3AweGY5Mm1ueHlhaWl0YXdtIn0.1nuiwQqcap38GeVekTrj0A',
        center=dict(lat=df['breitengrad'].mean(), lon=df['laengengrad'].mean()),
        zoom=6.2
    )
)

# Karte anzeigen
fig.show()
