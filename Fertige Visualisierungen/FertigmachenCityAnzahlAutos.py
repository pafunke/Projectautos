import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os

#dadurch sollte Data frame immer erkannt werden solange er im selben Ordner liegt
csvDatei = 'cleaned_electric_cars_data_final.csv'
csv_path = os.path.join(os.path.dirname(__file__), csvDatei)
df = pd.read_csv(csv_path)

##funktioniert nur an meinem laptop
#df = pd.read_csv('/Users/patrickfunke/CodeHub/Projectautos/data/cleaned_electric_cars_data_final.csv')

token = 'pk.eyJ1Ijoid2kyMzA0NCIsImEiOiJjbHUzNnhkN3AweGY5Mm1ueHlhaWl0YXdtIn0.1nuiwQqcap38GeVekTrj0A'


# colors = [
#     [0, 'rgb(173, 216, 230)'],  #Hellblau
#     [1, 'rgb(144, 238, 144)']   #Hellgrün
# ]

# Farbscala nach log, da kleine zu klein und seattle zu groß
def get_log_color(count):
    maxAnzahlAutos = np.log(df['City'].value_counts().max() + 1)
    minAnzahlAutos = np.log(df['City'].value_counts().min() + 1)
    normalized_count = (np.log(count + 1) - minAnzahlAutos) / (maxAnzahlAutos - minAnzahlAutos)
    color_scale = np.clip(normalized_count, 0, 30000) 
    color = (int(0 + (144 - 0) * color_scale), int(0 + (238 - 0) * color_scale), int(255 + (144 - 255) * color_scale))
    ## Für den test erst colors Auskommentieren und coors oben entkommentieren
    # print(maxAnzahlAutos)
    # print(minAnzahlAutos)

    return f'rgb{color}'

# liste für skala von 0 bsi 30000 schrittweite 100
farbenfürFarbverlauf = np.linspace(0, 30000, 100)

# Farbverlauf für skala aus logarithmischer Funktion für Marker erstellen
colors = [get_log_color(farbwerinFarbe) for farbwerinFarbe in farbenfürFarbverlauf]

# Karte erstellen -> muss über Scatter sein
fig = go.Figure()

# Städte hinzufügen
for city in df['City'].unique():
    city_data = df[df['City'] == city]
    anzahlAutosCity = city_data.shape[0]  # Anzahl der einzigartigen Fahrzeuge in der Stadt
    if anzahlAutosCity > 0:
        size = np.log(anzahlAutosCity + 1)*2  # Logarithmische Skalierung der Kreisgröße
    else:
        size = 3  # Mindestgröße für Städte ohne Fahrzeuge
        
    fig.add_trace(go.Scattermapbox(
        lat=[city_data.iloc[0]['breitengrad']],  # Breitengrad der Stadt
        lon=[city_data.iloc[0]['laengengrad']],  # Längengrad der Stadt
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=size,  # log anzahl fahrzeuge
            color=get_log_color(anzahlAutosCity),  # farbe in anzahl fahrzeuge
            opacity=0.6,  # Transparenz 
            colorscale= colors,

            #Skala tut noch nicht 
            #Skalierungsdaten lassen sich nicht anlegen??? -> keine lösung gefunden jetzt erstmal skala nur bei 0 
            colorbar= dict(
                title = 'Skala Anzahl Autos',
                tickvals=[0],  # Positionen tut aber nicht richtig desahalb 0
                ticktext=["0"],  # Beschriftung aber peoblem mit tickvals
                x=1.3  # Position der Farbskala auf der Karte  -> bei x.12 verdeckt srädte Namen              
            )
        ),
        
        #Vielleicht ncoh hinzufügen Hybride und Voll elektrisch
        #Dann aber nicht klar für was genau Visualisierung steht
        hoverinfo='text',
        hovertext=f"City: {city}<br>Total Vehicles: {anzahlAutosCity}",
        name=city
    ))

# Layout der Karte einstellen
fig.update_layout(
    mapbox=dict(
        accesstoken=token,
        center=dict(lat=df['breitengrad'].mean(), lon=df['laengengrad'].mean()),
        zoom=6.2
    )
)
# Karte anzeigen
fig.show()