import pandas as pd
import plotly.graph_objs
fig = plotly.graph_objects.Figure()
import os

df = pd.read_csv(os.path.join(os.path.dirname(__file__), '/Users/patrickfunke/CodeHub/Projectautos/data/cleaned_electric_cars_data_final.csv'), sep=',')



#Gruppieren in Farbgruppen
color_dict = {
    'battery electric vehicle (bev)': 'lightgreen',  
    'plug-in hybrid electric vehicle (phev)': 'lightblue',  
}

#für jede farbe in dictionary s.h oben extra datenpunkte erstellen
count = 0
data = [] #muss unbedingt data heißen wegen plotly

for ev_type, color in color_dict.items():
    ev_df = df[df['Electric Vehicle Type'] == ev_type]
    data.append(plotly.graph_objs.Scattermapbox(
        lat=ev_df['breitengrad'],  # Breitengrad
        lon=ev_df['laengengrad'],  # Längengrad
        mode='markers',
        marker=dict(
            size=9,
            color=color,  # Farbe basierend auf Elektrofahrzeugtyp
            opacity=0.7,
        ),
        text=ev_df[['Model', 'Make', 'Electric Vehicle Type']].astype(str),  # Anzeigetext für jeden Punkt
        name=ev_type  # Legendenname für den Elektrofahrzeugtyp
    ))

# Layout der Karte konfigurieren
layout = plotly.graph_objs.Layout(
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken='pk.eyJ1Ijoid2kyMzA0NCIsImEiOiJjbHUzNnhkN3AweGY5Mm1ueHlhaWl0YXdtIn0.1nuiwQqcap38GeVekTrj0A', 
        #style='streets',  # Kartentyp (z.B. 'streets', 'satellite', 'dark', 'light', etc.)
        bearing=0,
        center=dict(
            #Startunkt Karte
            lat=df['breitengrad'].mean(),lon=df['laengengrad'].mean()
            ),
        pitch=0,
        zoom=6.2, 
    )
)
#Karte erstellen
fig = plotly.graph_objs.Figure(data=data, layout=layout)

# Karte anzeigen
fig.show()
