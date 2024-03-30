import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os
df = pd.read_csv(os.path.join(os.path.dirname(__file__), '/Users/patrickfunke/CodeHub/Projectautos/data/cleaned_electric_cars_data_final.csv'), sep=',')
fig = go.Figure()


# Farbscala nach log, da kleine zu klein und seattle zu groß
def get_log_color(count):
    max_count = np.log(df['City'].value_counts().max() + 1)
    min_count = np.log(df['City'].value_counts().min() + 1)
    normalized_count = (np.log(count + 1) - min_count) / (max_count - min_count)
    
    # Definiere den Farbverlauf von Blau zu Grün
    start_color = [173, 216, 230]  # Blau
    end_color = [144, 238, 144]  # Grün
    
    # Passen Sie die Gewichtung des Grüns basierend auf der Normalisierung an
    green_weight = normalized_count ** 3  # Stärkere Gewichtung des Grüns später
    
    # Lineare Interpolation zwischen den Farben entsprechend der Gewichtung
    color = [
        int(start_color[i] + (end_color[i] - start_color[i]) * green_weight)
        for i in range(3)
    ]
    
    return f'rgb({color[0]}, {color[1]}, {color[2]})'

# Erstellen der Farbskala
color_scale_list = []
tick_texts = []
unique_normalized_values = sorted(set(np.linspace(0, 1, 5)))  # 5 eindeutige Normalisierungswerte
for normalized_value in unique_normalized_values:
    tick_texts.append(f'{normalized_value:.2f}')  # Füge die Normalisierungswerte als Ticktexte hinzu
    color_scale_list.append([normalized_value, get_log_color(normalized_value * (df['City'].value_counts().max() - df['City'].value_counts().min()))])

# Karte erstellen
fig = go.Figure()

# Städte hinzufügen
for city in df['City'].unique():
    city_data = df[df['City'] == city]
    city_vehicle_count = city_data.shape[0]  # Anzahl der einzigartigen Fahrzeuge in der Stadt
    if city_vehicle_count > 0:
        size = np.log(city_vehicle_count + 1)*2  # Logarithmische Skalierung der Kreisgröße
    else:
        size = 3  # Mindestgröße für Städte ohne Fahrzeuge
    fig.add_trace(go.Scattermapbox(
        lat=[city_data.iloc[0]['breitengrad']],  # Breitengrad der Stadt
        lon=[city_data.iloc[0]['laengengrad']],  # Längengrad der Stadt
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=size,  # log anzahl fahrzeuge
            color=get_log_color(city_vehicle_count),  # farbe in anzahl fahrzeuge
            opacity=0.6,  # Transparenz
            colorscale=color_scale_list,  # Verwendung der erstellten Farbskala
            colorbar=dict(
                title='Anzahl der Fahrzeuge',
                tickvals=unique_normalized_values,  # Positionen der Tickmarken auf der Farbskala
                ticktext=tick_texts,  # Verwenden der vorbereiteten Ticktexte
                len=1,  # Länge der Farbskala relativ zur Kartenbreite
                yanchor="top",  # Verankerung der Farbskala oben
                y=1,  # Position der Farbskala relativ zur Kartenhöhe
                x=1.3
            )
        ),
        hoverinfo='text',
        hovertext=f"City: {city}<br>Total Vehicles: {city_vehicle_count}",
        name=city
    ))

# Layout der Karte einstellen
fig.update_layout(
    mapbox=dict(
        accesstoken='pk.eyJ1Ijoid2kyMzA0NCIsImEiOiJjbHUzNnhkN3AweGY5Mm1ueHlhaWl0YXdtIn0.1nuiwQqcap38GeVekTrj0A',
        center=dict(lat=df['breitengrad'].mean(), lon=df['laengengrad'].mean()),
        zoom=6.2
    )
)

# Karte anzeigen
fig.show()
