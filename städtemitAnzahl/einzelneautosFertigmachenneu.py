import pandas as pd
import plotly.graph_objs as go
import os

df = pd.read_csv(os.path.join(os.path.dirname(__file__), '/Users/patrickfunke/CodeHub/Projectautos/Fertige Visualisierungen/cleaned_electric_cars_data_final.csv'), sep=',')

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
    text = grouped.apply(lambda row: "<br>".join([f"Model: {model}, Make: {make}, Type: {elec_vehicle_type}" for model, make in zip(row['Model'], row['Make'])]), axis=1)
    data.append(go.Scattermapbox(
        lat=grouped['breitengrad'],
        lon=grouped['laengengrad'],
        mode='markers',
        marker=dict(
            size=9,
            color=color,
            opacity=0.4,
        ),
        text=text,
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
layout = go.Layout(mapbox=mapbox_config)

# Karte erstellen
fig = go.Figure(data=data, layout=layout)

# Karte anzeigen
fig.show()
