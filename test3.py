import pandas as pd
import plotly.graph_objects as go
import os

df = pd.read_csv(os.path.join(os.path.dirname(__file__), '/Users/patrickfunke/CodeHub/Projectautos/data/cleaned_electric_cars_data_final.csv'), sep=',')
fig = go.Figure()

# Gruppieren in Farbgruppen
color_dict = {
    'battery electric vehicle (bev)': 'lightgreen',  
    'plug-in hybrid electric vehicle (phev)': 'lightblue',  
}

# Für jede Farbe im Dictionary Datenpunkte erstellen
data = []
for typeelecvehic, color in color_dict.items():
    dataelecvehic = df[df['Electric Vehicle Type'] == typeelecvehic]
    data.append(go.Scattermapbox(
        lat=dataelecvehic['breitengrad'],  # Breitengrad
        lon=dataelecvehic['laengengrad'],  # Längengrad
        mode='markers',
        marker=dict(
            size=9,
            color=color,  # Farbe basierend auf Elektrofahrzeugtyp
            opacity=0.7,
        ),
        text=dataelecvehic[['Model', 'Make', 'Electric Vehicle Type']].astype(str),  # Anzeigetext für jeden Punkt
        name=typeelecvehic  # Legendenname für den Elektrofahrzeugtyp
    ))

# Konfiguration für Mapbox-Karte
mapbox_config = {
    'accesstoken': 'pk.eyJ1Ijoid2kyMzA0NCIsImEiOiJjbHUzNnhkN3AweGY5Mm1ueHlhaWl0YXdtIn0.1nuiwQqcap38GeVekTrj0A', 
    'bearing': 0,
    'center': {'lat': df['breitengrad'].mean(), 'lon': df['laengengrad'].mean()},
    'pitch': 0,
    'zoom': 6.2
}

# Layout der Karte konfigurieren
layout = go.Layout(mapbox=mapbox_config)

# Karte erstellen
fig = go.Figure(data=data, layout=layout)

# Karte anzeigen
fig.show()
