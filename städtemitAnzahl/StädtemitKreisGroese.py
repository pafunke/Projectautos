import plotly.graph_objects as go
import pandas as pd

# Daten aus CSV-Datei lesen
df = pd.read_csv('/Users/patrickfunke/CodeHub/Projectautos/Fertige Visualisierungen/cleaned_electric_cars_data_final.csv')

# Mapbox Token setzen
token = 'pk.eyJ1Ijoid2kyMzA0NCIsImEiOiJjbHUzNnhkN3AweGY5Mm1ueHlhaWl0YXdtIn0.1nuiwQqcap38GeVekTrj0A'

# Karte erstellen
fig = go.Figure()

# Städte hinzufügen
for city in df['City'].unique():
    city_data = df[df['City'] == city]
    city_vehicle_count = city_data.shape[0]  # Anzahl der einzigartigen Fahrzeuge in der Stadt
    fig.add_trace(go.Scattermapbox(
        lat=[city_data.iloc[0]['breitengrad']],  # Breitengrad der Stadt
        lon=[city_data.iloc[0]['laengengrad']],  # Längengrad der Stadt
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=city_vehicle_count/200,  # Kreisgröße basierend auf der Anzahl der einzigartigen Fahrzeuge
            color='blue',  # Farbe der Marker
            opacity=0.3  # Transparenz der Marker
        ),
        hoverinfo='text',
        hovertext=f"City: {city}<br>Total Vehicles: {city_vehicle_count}",
        name=city
    ))

# Layout der Karte einstellen
fig.update_layout(
    mapbox=dict(
        accesstoken=token,
        center=dict(lat=df['breitengrad'].mean(), lon=df['laengengrad'].mean()),
        zoom=6.2
    )
)

# Karte anzeigen
fig.show()
