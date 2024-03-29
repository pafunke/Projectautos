import pandas as pd
import plotly.graph_objects as go
import json

# Laden des Datensatzes mit Airbnb-Listings
df = pd.read_csv('/Users/patrickfunke/src/DS101_DV/data/listings_subset_cleaned.csv', sep=',')

# Laden der GeoJSON-Daten für Berliner Stadtteile


# Festlegen der IDs für die GeoJSON-Eigenschaften
for feature in geo_data['features']:
    feature['id'] = feature['properties']['Gemeinde_name']

# Berechnen des Durchschnitts der Preise nach Stadtteil
df_group_mean = df.groupby('neighbourhood_group_cleansed').mean(numeric_only=True)

# Erstellen der Choroplethenkarte
choropleth = go.Choroplethmapbox(
    geojson=geo_data,
    locations=df_group_mean.index,
    z=df_group_mean.price,
    marker_opacity=0.7,
    marker_line_width=0,
    colorscale='GnBu'
)

# Erstellen der Scatterpunkte für Airbnb-Listings
scatter = go.Scattermapbox(
    lat=df['latitude'],
    lon=df['longitude'],
    mode='markers',
    marker=dict(
        size=df['beds'].fillna(1),
        color=df['price'],
        cmax=130,
        cmin=30,
        showscale=True
    ),
    text=df['host_name']
)

# Erstellen der Figur und Hinzufügen der Trace
fig = go.Figure()
fig.add_trace(choropleth)
fig.add_trace(scatter)

# Layout der Karte konfigurieren
fig.update_layout(
    mapbox_style="light",
    mapbox_accesstoken='pk.eyJ1Ijoid2kyMzA0NCIsImEiOiJjbHUzNnhkN3AweGY5Mm1ueHlhaWl0YXdtIn0.1nuiwQqcap38GeVekTrj0A',
    mapbox_zoom=10,
    mapbox_center={"lat": 52.520008, "lon": 13.404954}
)

# Anzeigen der Karte
fig.show()

# Speichern der Karte als HTML-Datei
fig.write_html("map.html", auto_open=True)
