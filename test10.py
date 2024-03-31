import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Daten aus CSV-Datei lesen
df = pd.read_csv('/Users/patrickfunke/CodeHub/Projectautos/data/cleaned_electric_cars_data_final.csv')

# Farbscala nach log, da kleine zu klein und seattle zu groß
def get_log_color(count):
    max_count = np.log(df['City'].value_counts().max() + 1)
    min_count = np.log(df['City'].value_counts().min() + 1)
    normalized_count = (np.log(count + 1) - min_count) / (max_count - min_count)
    color_scale = np.clip(normalized_count, 0, 1) 
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

# Farbskala für die Legende erstellen
color_scale_data = np.linspace(0, 1, 100)  # 100 Schritte für die Farbskala
colors = [get_log_color(value) for value in color_scale_data]

# Legende für die Farbskala erstellen
legend = go.Scattermapbox(
    lat=[],
    lon=[],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=0,  # Größe der Marker auf 0 setzen
        color=color_scale_data,
        colorscale=colors,
        colorbar=dict(
            title='Anzahl der Fahrzeuge',
            tickvals=[0, 1],
            ticktext=['0', '30000'],
            x=1.1,  # Position der Farbskala auf der Karte
            len=0.75  # Länge der Farbskala
        )
    ),
    showlegend=False
)

# Legende zur Karte hinzufügen
fig.add_trace(legend)

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
