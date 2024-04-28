import pandas as pd
import plotly.graph_objs as go
import os

csvDatei = 'cleaned_electric_cars_data_final.csv'
csvPath = os.path.join(os.path.dirname(__file__), csvDatei)
df = pd.read_csv(csvPath)

# Elektrofahrzeugtypen und zugehörige Farben definieren
color_dict = {
    'battery electric vehicle (bev)': 'lightgreen',  
    'plug-in hybrid electric vehicle (phev)': 'lightblue',  
}

# Daten für jeden Elektrofahrzeugtyp vorbereiten
data = []
for elec_vehicle_type, color in color_dict.items():
    data_elevech = df[df['Electric Vehicle Type'] == elec_vehicle_type]
    grouped = data_elevech.groupby(['breitengrad', 'laengengrad'])[['Model', 'Make', 'Electric Vehicle Type']].agg(list).reset_index()
    #special abfrage, liegt es an meinem laptop, dass es nicht lädt?
    #M2 Max deutlich flüssiger aber nur mit dieser Implementierung getestet
    ausgabePunkte = grouped.apply(lambda row: "<br>".join([f"Model: {model}, Make: {make}, Type: {elec_vehicle_type}" for model, make in zip(row['Model'], row['Make'])]) if len(set(row['Model'])) <= 35 else f"Total Models: {len(set(row['Model']))}", axis=1)
    data.append(go.Scattermapbox(
        lat=grouped['breitengrad'],
        lon=grouped['laengengrad'],
        mode='markers',
        marker=dict(
            size=9,
            color=color,
            opacity=0.4,
        ),
        text=ausgabePunkte,
        name=elec_vehicle_type
    ))

# Mapbox-Konfiguration
mapbox_config = {
    'accesstoken': 'pk.eyJ1Ijoid2kyMzA0NCIsImEiOiJjbHUzNnhkN3AweGY5Mm1ueHlhaWl0YXdtIn0.1nuiwQqcap38GeVekTrj0A', 
    'bearing': 0,
    'center': {'lat': df['breitengrad'].mean(), 'lon': df['laengengrad'].mean()},
    'pitch': 0,
    'zoom': 6.2
}

# Layout der Karte
layout = go.Layout(mapbox=mapbox_config, title='Elektro- und Hybridauto-Standorte')

# Karte erstellen
fig = go.Figure(data=data, layout=layout)

# Karte anzeigen
fig.show()
