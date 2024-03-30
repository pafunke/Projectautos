import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Daten aus CSV-Datei lesen
df = pd.read_csv('/Users/patrickfunke/CodeHub/Projectautos/data/cleaned_electric_cars_data_final.csv')

# Mapbox Token setzen
token = 'YOUR_MAPBOX_TOKEN'

# Funktion zur logarithmischen Farbskala
def get_log_color(count):
    # Logarithmische Skalierung der Farbwerte basierend auf der Anzahl der Fahrzeuge
    max_count = np.log(df['City'].value_counts().max() + 1)
    min_count = np.log(df['City'].value_counts().min() + 1)
    normalized_count = (np.log(count + 1) - min_count) / (max_count - min_count)
    color_scale = np.clip(normalized_count, 0, 1)  # Clip-Werte auf Bereich von 0 bis 1
    # Interpolation zwischen hellblau (0, 0, 255) und hellgrün (144, 238, 144)
    color = (int(0 + (144 - 0) * color_scale), int(0 + (238 - 0) * color_scale), int(255 + (144 - 255) * color_scale))
    return f'rgb{color}'

# Karte erstellen
fig = go.Figure()

# Städte hinzufügen
for city in df['City'].unique():
    city_data = df[df['City'] == city]
    city_vehicle_count = city_data.shape[0]  # Anzahl der einzigartigen Fahrzeuge in der Stadt
    if city_vehicle_count > 0:
        size = np.log(city_vehicle_count + 1)*2  # Logarithmische Skalierung der Kreisgröße
    else:
        size = 3  # Mindestgröße für Städte ohne Fahrzeuge
    fig.add_trace(go.Scattermapbox(
        lat=[city_data.iloc[0]['breitengrad']],  # Breitengrad der Stadt
        lon=[city_data.iloc[0]['laengengrad']],  # Längengrad der Stadt
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=size,  # log anzahl fahrzeuge
            color=get_log_color(city_vehicle_count),  # farbe in anzahl fahrzeuge
            opacity=0.6,  # Transparenz 
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

# tut nicht:

fig.update_layout(
    coloraxis_colorbar=dict(
        title="Anzahl der Fahrzeuge",  # Titel der Farbskala
        tickvals=[0, 0.5, 1],  # Positionen der Tickmarken auf der Farbskala
        ticktext=["Niedrig", "Mittel", "Hoch"],  # Beschriftungen der Tickmarken auf der Farbskala
        len=0.75,  # Länge der Farbskala relativ zur Kartenbreite
        yanchor="top",  # Verankerung der Farbskala oben
        y=0.9,  # Position der Farbskala relativ zur Kartenhöhe
    )
)

# Karte anzeigen
fig.show()
