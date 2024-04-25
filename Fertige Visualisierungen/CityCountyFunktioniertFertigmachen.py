import plotly.graph_objects
import pandas as pd
import numpy as np
import os

csvDatei = 'cleaned_electric_cars_data_final.csv'
csv_path = os.path.join(os.path.dirname(__file__), csvDatei)
df = pd.read_csv(csv_path)

token = 'pk.eyJ1Ijoid2kyMzA0NCIsImEiOiJjbHUzNnhkN3AweGY5Mm1ueHlhaWl0YXdtIn0.1nuiwQqcap38GeVekTrj0A'

def get_log_color(count):
    maxAnzahlAutos = np.log(df['City'].value_counts().max() + 1)
    minAnzahlAutos = np.log(df['City'].value_counts().min() + 1)
    normalized_count = (np.log(count + 1) - minAnzahlAutos) / (maxAnzahlAutos - minAnzahlAutos)
    color_scale = np.clip(normalized_count, 0, 30000) 
    color = (int(0 + (144 - 0) * color_scale), int(0 + (238 - 0) * color_scale), int(255 + (144 - 255) * color_scale))
    return f'rgb{color}'

# Farbskala für die Marker erstellen
farbenfürFarbverlauf = np.linspace(0, 30000, 100)
colors = [get_log_color(farbwerinFarbe) for farbwerinFarbe in farbenfürFarbverlauf]

# Anzeigen Elektro + Hybride und alle Autos
def get_hover_text(city_or_county, location, num_bevs, num_phevs, total):
    return f"{city_or_county}: {location}<br>Total BEVs: {num_bevs}<br>Total PHEVs: {num_phevs}<br>Total Vehicles: {total}"

# Karte erstellen
fig = plotly.graph_objects.Figure()

# Städte hinzufügen
for city in df['City'].unique():
    city_data = df[df['City'] == city]
    num_bevs = city_data[city_data["Electric Vehicle Type"].str.lower() == "battery electric vehicle (bev)"].shape[0]
    num_phevs = city_data[city_data["Electric Vehicle Type"].str.lower() == "plug-in hybrid electric vehicle (phev)"].shape[0]
    total_vehicles = num_bevs + num_phevs

    if total_vehicles > 0:
        size = np.log(total_vehicles + 1) * 2
    else:
        size = 3

    fig.add_trace(plotly.graph_objects.Scattermapbox(
        lat=[city_data.iloc[0]['breitengrad']],
        lon=[city_data.iloc[0]['laengengrad']],
        mode='markers',
        marker=plotly.graph_objects.scattermapbox.Marker(
            size=size,
            color=get_log_color(total_vehicles),
            opacity=0.6,
            colorscale=colors,
        ),
        hoverinfo='text',
        hovertext=get_hover_text("City", city, num_bevs, num_phevs, total_vehicles),
        name=city
    ))

# Landkreise hinzufügen
for county in df['County'].unique():
    county_data = df[df['County'] == county]
    num_bevs = county_data[county_data["Electric Vehicle Type"].str.lower() == "battery electric vehicle (bev)"].shape[0]
    num_phevs = county_data[county_data["Electric Vehicle Type"].str.lower() == "plug-in hybrid electric vehicle (phev)"].shape[0]
    total_vehicles = num_bevs + num_phevs

    if total_vehicles > 0:
        size = np.log(total_vehicles + 1) * 2
    else:
        size = 3

    fig.add_trace(plotly.graph_objects.Scattermapbox(
        lat=[county_data.iloc[0]['breitengrad']],
        lon=[county_data.iloc[0]['laengengrad']],
        mode='markers',
        marker=plotly.graph_objects.scattermapbox.Marker(
            size=size,
            color=get_log_color(total_vehicles),
            opacity=0.6,
            colorscale=colors,
            #showscale= True
        ),
        hoverinfo='text',
        hovertext=get_hover_text("County", county, num_bevs, num_phevs, total_vehicles),
        name=county
    ))

# Layout der Karte einstellen
fig.update_layout(
    mapbox=dict(
        accesstoken=token,
        center=dict(lat=df['breitengrad'].mean(), lon=df['laengengrad'].mean()),
        zoom=6.2
    )
)

#einzelne buttons city county (drop down hat nicht geklappt)
fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            active=0,
            x=0.5,
            y=1.2,
            buttons=list([
                dict(label="City",
                     method="update",
                     args=[{"visible": [True] * len(df['City'].unique()) + [False] * len(df['County'].unique())}, {"title": "Electric Vehicles Distribution per City"}]),
                dict(label="County",
                     method="update",
                     args=[{"visible": [False] * len(df['City'].unique()) + [True] * len(df['County'].unique())}, {"title": "Electric Vehicles Distribution per County"}])
            ]),
        )
    ]
)

# Karte anzeigen
fig.show()
