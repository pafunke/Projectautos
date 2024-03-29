import pandas as pd
import plotly.graph_objs
fig = plotly.graph_objects.Figure()

# Laden des Datensatzes mit Längen- und Breitengradkoordinaten der Elektroautos
df = pd.read_csv('cleaned_electric_cars_data.csv')

# Erstellen der Datenpunkte für die Karte
# data = [
#     plotly.graph_objs.Scattermapbox(
#         lat=df['breitengrad'],  # Breitengrad
#         lon=df['laengengrad'],  # Längengrad
#         mode='markers',
#         marker=dict(
#             size=9,
#             color ='green',
#             opacity=0.7,
#         ),
#        text = df[['Model', 'Make', 'Electric Vehicle Type']].astype(str) # Anzeigetext für jeden Punkt (z.B. Modell des Elektroautos)
#     )
# ]



color_dict = {
    'battery electric vehicle (bev)': 'lightgreen',  # Beispiel: Blau für BEVs
    'plug-in hybrid electric vehicle (phev)': 'lightblue',  # Beispiel: Rot für PHEVs
    # Fügen Sie weitere Elektrofahrzeugtypen und entsprechende Farben hinzu, falls erforderlich
}

# Erstellen der Datenpunkte für die Karte
data = []
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
        style='streets',  # Kartentyp (z.B. 'streets', 'satellite', 'dark', 'light', etc.)
        bearing=0,
        center=dict(
            #Startunkt Karte
            lat=df['breitengrad'].mean(),lon=df['laengengrad'].mean()  
        ),
        pitch=0,
        zoom=6.4, 
    )
)


##Test code 
# fig.update_layout(
#     mapbox_style="light",
#     mapbox_accesstoken='pk.eyJ1Ijoid2kyMzA0NCIsImEiOiJjbHUzNnhkN3AweGY5Mm1ueHlhaWl0YXdtIn0.1nuiwQqcap38GeVekTrj0A',
#     mapbox_zoom=6.4,
#     mapbox_center=dict(      
#         lat=df['breitengrad'].mean(),  #Karte startet aam richtigen platz
#         lon=df['laengengrad'].mean(), 
#     )  
# )

#Karte erstellen
fig = plotly.graph_objs.Figure(data=data, layout=layout)

##Test Code
# fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
# fig.show()
# fig.write_html("map.html", auto_open=True)

# Karte anzeigen
fig.show()
