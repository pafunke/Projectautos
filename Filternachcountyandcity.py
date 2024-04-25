import pandas as pd
import plotly.graph_objs as go
import os

# Lesen der Daten
df = pd.read_csv('Users/patrickfunke/CodeHub/Projectautos/Fertige Visualisierungen/cleaned_electric_cars_data_final.csv')

# Funktion zum Erstellen des Karteninhalts
def create_map_data(df, location_type=None, location=None):
    # Filtern nach 'County' und 'City', je nach Auswahl
    if location_type == 'County':
        df = df[df['County'] == location]
    elif location_type == 'City':
        df = df[df['City'] == location]

    # Gruppieren nach 'Electric Vehicle Type' und Zählen der Anzahl von Fahrzeugen
    grouped = df.groupby(['Electric Vehicle Type']).size().reset_index(name='count')
    
    data = []
    for index, row in grouped.iterrows():
        typeelecvehic = row['Electric Vehicle Type']
        count = row['count']
        color = color_dict.get(typeelecvehic, 'gray')  # Verwenden Sie 'gray' als Standardfarbe, wenn nicht gefunden
        
        dataelecvehic = df[df['Electric Vehicle Type'] == typeelecvehic]
        data.append(go.Scattermapbox(
            lat=dataelecvehic['breitengrad'],  # Breitengrad
            lon=dataelecvehic['laengengrad'],  # Längengrad
            mode='markers',
            marker=dict(
                size=count/9999,  # Anpassen der Punktegröße basierend auf der Anzahl der Fahrzeuge
                color=color,  # Farbe basierend auf Elektrofahrzeugtyp
                opacity=0.7,
            ),
            text=dataelecvehic[['Model', 'Make', 'Electric Vehicle Type']].astype(str),  # Anzeigetext für jeden Punkt
            name=typeelecvehic  # Legendenname für den Elektrofahrzeugtyp
        ))
    return data

# Gruppieren in Farbgruppen
color_dict = {
    'battery electric vehicle (bev)': 'lightgreen',  
    'plug-in hybrid electric vehicle (phev)': 'lightblue',  
}

mapboxLayout = {
    'accesstoken': 'pk.eyJ1Ijoid2kyMzA0NCIsImEiOiJjbHUzNnhkN3AweGY5Mm1ueHlhaWl0YXdtIn0.1nuiwQqcap38GeVekTrj0A', 
    'center': {'lat': df['breitengrad'].mean(), 'lon': df['laengengrad'].mean()},
    'zoom': 6.2
}

# Layout der Karte konfigurieren
layout = go.Layout(mapbox=mapboxLayout)

# Karte erstellen
fig = go.Figure(layout=layout)

# Buttons erstellen
buttons = [
    dict(label='County', method='update', args=[{'visible': True}, {'location_type': 'County'}]),
    dict(label='City', method='update', args=[{'visible': True}, {'location_type': 'City'}])
]

# Filter für 'County' und 'City'
county = None
city = None

# Karteninhalt erstellen
data = create_map_data(df, None, None)

# Daten zur Karte hinzufügen
for trace in data:
    fig.add_trace(trace)

# Karte anzeigen
fig.update_layout(
    mapbox=mapboxLayout,
    updatemenus=[
        dict(
            buttons=buttons,
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.1,
            yanchor="top"
        ),
    ]
)
fig.show()
