import pandas as pd
import plotly.graph_objs
import os

df = pd.read_csv(os.path.join(os.path.dirname(__file__), '/Users/patrickfunke/CodeHub/Projectautos/data/cleaned_electric_cars_data_final.csv'), sep=',')
fig = plotly.graph_objects.Figure()


#Gruppieren in Farbgruppen
color_dict = {
    'battery electric vehicle (bev)': 'lightgreen',  
    'plug-in hybrid electric vehicle (phev)': 'lightblue',  
}

#für jede farbe in dictionary s.h oben extra datenpunkte erstellen
count = 0
data = [] #muss unbedingt data heißen wegen plotly

for typeelecvehic, color in color_dict.items():
    dataelecvehic = df[df['Electric Vehicle Type'] == typeelecvehic]
    data.append(plotly.graph_objs.Scattermapbox(
        lat=dataelecvehic['breitengrad'],  # Breitengrad
        lon=dataelecvehic['laengengrad'],  # Längengrad
        mode='markers',
        marker=dict(
            size=9,
            color=color,  # Farbe basierend auf Elektrofahrzeugtyp
            opacity=0.4,
        ),
        text=dataelecvehic[['Model', 'Make', 'Electric Vehicle Type']].astype(str),  # Anzeigetext für jeden Punkt
        # Anzeigetext für jeden Punkt

        name=typeelecvehic  # Legendenname für den Elektrofahrzeugtyp
    ))
    count += len(dataelecvehic)

print("anzahl Einträge:", count)

#kann weg prüfen:

# #Layout der Karte konfigurieren
# layout = plotly.graph_objs.Layout(
#     mapbox=dict(
#         accesstoken='pk.eyJ1Ijoid2kyMzA0NCIsImEiOiJjbHUzNnhkN3AweGY5Mm1ueHlhaWl0YXdtIn0.1nuiwQqcap38GeVekTrj0A', 
#         #style='streets',  # Kartentyp (z.B. 'streets', 'satellite', 'dark', 'light', etc.)
#         bearing=0,
#         center=dict(
#             #Startunkt Karte
#             lat=df['breitengrad'].mean(),lon=df['laengengrad'].mean()
#             ),
#         pitch=0,
#         zoom=6.2, 
#     )
# )
    
mapbox_config = {
    'accesstoken': 'pk.eyJ1Ijoid2kyMzA0NCIsImEiOiJjbHUzNnhkN3AweGY5Mm1ueHlhaWl0YXdtIn0.1nuiwQqcap38GeVekTrj0A', 
    'bearing': 0,
    'center': {'lat': df['breitengrad'].mean(), 'lon': df['laengengrad'].mean()},
    'pitch': 0,
    'zoom': 6.2
}

# Layout der Karte konfigurieren
layout = plotly.graph_objs.Layout(mapbox=mapbox_config)

#Karte erstellen
fig = plotly.graph_objs.Figure(data=data, layout=layout)

# Karte anzeigen
fig.show()
