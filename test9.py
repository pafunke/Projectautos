import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Daten aus CSV-Datei lesen
df = pd.read_csv('/Users/patrickfunke/CodeHub/Projectautos/data/cleaned_electric_cars_data_final.csv')

# Mapbox Token setzen
token = 'YOUR_MAPBOX_TOKEN'
colors = [
    [0, 'rgb(173, 216, 230)'],  # Hellblau
    [1, 'rgb(144, 238, 144)']   # Hellgrün
]

# Farbscala nach log, da kleine zu klein und seattle zu groß
def get_log_color(count):
    max_count = np.log(df['City'].value_counts().max() + 1)
    min_count = np.log(df['City'].value_counts().min() + 1)
    normalized_count = (np.log(count + 1) - min_count) / (max_count - min_count)
    color_scale = np.clip(normalized_count, 0, 30000) 
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
            colorscale= colors,
            cmin=1,  # Minimalwert der Farbskala erhöht
            cmax=df['City'].value_counts().max(),  # Höchstwert der Farbskala
            colorbar=dict(
                title='skala Anzahl Autos',
                tickvals=[0, 0.5, 1],  # Positionen der Tickmarken auf der Farbskala
                ticktext=["Niedrig", "Mittel", "Hoch"],  # Beschriftungen der Tickmarken auf der Farbskala
                x=1.3  # Position der Farbskala auf der Karte
            )

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
