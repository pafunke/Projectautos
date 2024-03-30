import pandas as pd
import plotly.graph_objs as go

# Lesen der Daten
df = pd.read_csv('/Users/patrickfunke/CodeHub/Projectautos/data/cleaned_electric_cars_data_final.csv')

# Gruppieren nach Stadt und Elektrofahrzeugtyp
city_elec_count = df[df['Electric Vehicle Type'].isin(['battery electric vehicle (bev)', 'plug-in hybrid electric vehicle (phev)'])].groupby('City').size().reset_index(name='Electric Vehicles Count')
city_hybrid_count = df[df['Electric Vehicle Type'] == 'hybrid electric vehicle (hev)'].groupby('City').size().reset_index(name='Hybrid Vehicles Count')

# Zusammenführen der Daten
city_data = pd.merge(city_elec_count, city_hybrid_count, on='City', how='outer').fillna(0)

# Funktion zur Erstellung des Hover-Texts
def create_hover_text(city, bev_count, phev_count, hybrid_count):
    return f"Stadt: {city}<br>Elektroautos (BEV): {bev_count}<br>Elektroautos (PHEV): {phev_count}<br>Hybridautos: {hybrid_count}"

# Maximalanzahl von Elektroautos und Hybridautos
max_elec_count = max(city_data['Electric Vehicles Count'])
max_hybrid_count = max(city_data['Hybrid Vehicles Count'])

# Größe der Punkte relativ zur maximalen Anzahl der Fahrzeuge
sizes = (city_data['Electric Vehicles Count'] + city_data['Hybrid Vehicles Count']) / (max_elec_count + max_hybrid_count) * 30

# Karte erstellen
fig = go.Figure()

# Daten für Elektroautos (BEV) hinzufügen
fig.add_trace(go.Scattermapbox(
    lat=df[df['Electric Vehicle Type'] == 'battery electric vehicle (bev)']['breitengrad'],
    lon=df[df['Electric Vehicle Type'] == 'battery electric vehicle (bev)']['laengengrad'],
    mode='markers',
    marker=dict(
        size=sizes,
        color='lightblue',
        opacity=0.7,
    ),
    text=[create_hover_text(city, bev_count, phev_count, hybrid_count) for city, bev_count, phev_count, hybrid_count in zip(city_data['City'], city_data['Electric Vehicles Count'], city_data['Electric Vehicles Count'], city_data['Hybrid Vehicles Count'])],
    hoverinfo='text'
))

# Daten für Elektroautos (PHEV) hinzufügen
fig.add_trace(go.Scattermapbox(
    lat=df[df['Electric Vehicle Type'] == 'plug-in hybrid electric vehicle (phev)']['breitengrad'],
    lon=df[df['Electric Vehicle Type'] == 'plug-in hybrid electric vehicle (phev)']['laengengrad'],
    mode='markers',
    marker=dict(
        size=sizes,
        color='lightgreen',
        opacity=0.7,
    ),
    text=[create_hover_text(city, bev_count, phev_count, hybrid_count) for city, bev_count, phev_count, hybrid_count in zip(city_data['City'], city_data['Electric Vehicles Count'], city_data['Electric Vehicles Count'], city_data['Hybrid Vehicles Count'])],
    hoverinfo='text'
))

# Daten für Hybridautos hinzufügen
fig.add_trace(go.Scattermapbox(
    lat=df[df['Electric Vehicle Type'] == 'hybrid electric vehicle (hev)']['breitengrad'],
    lon=df[df['Electric Vehicle Type'] == 'hybrid electric vehicle (hev)']['laengengrad'],
    mode='markers',
    marker=dict(
        size=sizes,
        color='orange',
        opacity=0.7,
    ),
    text=[create_hover_text(city, bev_count, phev_count, hybrid_count) for city, bev_count, phev_count, hybrid_count in zip(city_data['City'], city_data['Electric Vehicles Count'], city_data['Electric Vehicles Count'], city_data['Hybrid Vehicles Count'])],
    hoverinfo='text'
))

# Layout der Karte konfigurieren
fig.update_layout(
    mapbox=dict(
        accesstoken='pk.eyJ1Ijoid2kyMzA0NCIsImEiOiJjbHUzNnhkN3AweGY5Mm1ueHlhaWl0YXdtIn0.1nuiwQqcap38GeVekTrj0A',
        center=dict(lat=df['breitengrad'].mean(), lon=df['laengengrad'].mean()),
        zoom=6.2
    )
)

# Karte anzeigen
fig.show()
