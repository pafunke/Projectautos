import plotly.graph_objects as go
import pandas as pd

# Daten erstellen
data = {
    'City': ['Seattle', 'Bothell', 'Seattle', 'Issaquah', 'Suquamish', 'Yelm', 'Yakima', 'Bothell', 'Port Orchard', 'Auburn', 'Seattle', 'Bainbridge Island', 'Yakima', 'Lynnwood'],
    'Vehicle Type': ['battery electric vehicle (bev)', 'battery electric vehicle (bev)', 'battery electric vehicle (bev)', 'battery electric vehicle (bev)', 'battery electric vehicle (bev)', 'plug-in hybrid electric vehicle (phev)', 'battery electric vehicle (bev)', 'plug-in hybrid electric vehicle (phev)', 'battery electric vehicle (bev)', 'battery electric vehicle (bev)', 'battery electric vehicle (bev)', 'battery electric vehicle (bev)', 'plug-in hybrid electric vehicle (phev)', 'battery electric vehicle (bev)']
}
df = pd.DataFrame(data)

# Mapbox Token setzen
mapbox_token = 'Ypk.eyJ1Ijoid2kyMzA0NCIsImEiOiJjbHUzNnhkN3AweGY5Mm1ueHlhaWl0YXdtIn0.1nuiwQqcap38GeVekTrj0A'

# Karte erstellen
fig = go.Figure()

# Städte hinzufügen
for city in df['City'].unique():
    city_data = df[df['City'] == city]
    fig.add_trace(go.Scattermapbox(
        lat=[47.6062],  # Latituden der Stadt, hier habe ich Seattle als Beispiel genommen
        lon=[-122.3321],  # Longituden der Stadt, hier habe ich Seattle als Beispiel genommen
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=10,
            color='blue',  # Du kannst die Farbe basierend auf dem Fahrzeugtyp ändern, wenn du möchtest
            opacity=0.7
        ),
        hoverinfo='text',
        hovertext=[f"City: {city}<br>Vehicle Type: {vtype}" for vtype in city_data['Vehicle Type']],
        name=city
    ))

# Layout der Karte einstellen
fig.update_layout(
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_token,
        style='light',  # Du kannst den Stil der Karte ändern, z.B. 'dark', 'satellite', etc.
        center=dict(
            lat=47.6062,  # Hier kannst du die Zentrum-Koordinaten der Karte ändern
            lon=-122.3321  # Hier kannst du die Zentrum-Koordinaten der Karte ändern
        ),
        zoom=5  # Hier kannst du den Zoom-Level der Karte ändern
    )
)

# Karte anzeigen
fig.show()
