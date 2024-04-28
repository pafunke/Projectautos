import plotly.graph_objects
import pandas as pd
import numpy as np
import os

csvDatei = 'cleaned_electric_cars_data_final.csv'
csvPath = os.path.join(os.path.dirname(__file__), csvDatei)
df = pd.read_csv(csvPath)
token = 'pk.eyJ1Ijoid2kyMzA0NCIsImEiOiJjbHUzNnhkN3AweGY5Mm1ueHlhaWl0YXdtIn0.1nuiwQqcap38GeVekTrj0A'



def get_log_color(count):
    maxAnzahlAutos = np.log(df['City'].value_counts().max() + 1)
    minAnzahlAutos = np.log(df['City'].value_counts().min() + 1)
    normalized_count = (np.log(count + 1) - minAnzahlAutos) / (maxAnzahlAutos - minAnzahlAutos)
    color_scale = np.clip(normalized_count, 0, 30000) 
    color = (int(0 + (144 - 0) * color_scale), 
             int(0 + (238 - 0) * color_scale), 
             int(255 + (144 - 255) * color_scale))
    return f'rgb{color}'

#Farbskala der Marker, dass es nicht die Standard farben sind
farbenfürFarbverlauf = np.linspace(0, 30000, 100)
colors = [get_log_color(farbwerinFarbe) for farbwerinFarbe in farbenfürFarbverlauf]

# Anzeigen Elektro + Hybride und alle Autos
def get_hover_text(city_or_county, location, anzahlElektros, anzahlHybride, total):
    return f"{city_or_county}: {location}<br>Total BEVs: {anzahlElektros}<br>Total PHEVs: {anzahlHybride}<br>Total Vehicles: {total}"

# ausgeb Obj.
fig = plotly.graph_objects.Figure()

# City : 1.Grafik
for city in df['City'].unique():
    datenStaedte = df[df['City'] == city]
    anzahlElektros = datenStaedte[datenStaedte["Electric Vehicle Type"].str.lower() == "battery electric vehicle (bev)"].shape[0]
    anzahlHybride = datenStaedte[datenStaedte["Electric Vehicle Type"].str.lower() == "plug-in hybrid electric vehicle (phev)"].shape[0]
    alleAutosAddiert = anzahlElektros + anzahlHybride

    if alleAutosAddiert > 0:
        size = np.log(alleAutosAddiert + 1) * 2
    else:
        size = 3

    fig.add_trace(plotly.graph_objects.Scattermapbox(

        lat=[datenStaedte.iloc[0]['breitengrad']],
        lon=[datenStaedte.iloc[0]['laengengrad']],
        mode='markers',
        marker=plotly.graph_objects.scattermapbox.Marker(
            size=size,
            color=get_log_color(alleAutosAddiert),
            opacity=0.6,
            colorscale=colors,
        ),

        hoverinfo='text',
        hovertext=get_hover_text("City", city, anzahlElektros, anzahlHybride, alleAutosAddiert),
        name=city,
        visible=True
    )
    )

# County :
for county in df['County'].unique():
    countyDaten = df[df['County'] == county]
    anzahlElektros = countyDaten[countyDaten["Electric Vehicle Type"].str.lower() == "battery electric vehicle (bev)"].shape[0]
    anzahlHybride = countyDaten[countyDaten["Electric Vehicle Type"].str.lower() == "plug-in hybrid electric vehicle (phev)"].shape[0]
    alleAutosAddiert = anzahlElektros + anzahlHybride

    if alleAutosAddiert > 0:
        size = np.log(alleAutosAddiert + 1) * 2
    else:
        size = 3

    fig.add_trace(plotly.graph_objects.Scattermapbox(
        lat=[countyDaten.iloc[0]['breitengrad']],
        lon=[countyDaten.iloc[0]['laengengrad']],
        mode='markers',
        marker=plotly.graph_objects.scattermapbox.Marker(
            size=size,
            color=get_log_color(alleAutosAddiert),
            opacity=0.6,
            colorscale=colors,
            #showscale= True # sieht einfach nicht gut aus
        ),

        hoverinfo='text',
        hovertext=get_hover_text("County", county, anzahlElektros, anzahlHybride, alleAutosAddiert),
        name=county,
        visible=False
    )
    )


# anpassen Karte
fig.update_layout(
    mapbox=dict(
        accesstoken=token,
        center=dict(lat=df['breitengrad'].mean(), lon=df['laengengrad'].mean()),
        zoom=6.2#sonst große Städte zu groß
    )
)



#einzelne buttons city county (drop down hat nicht geklappt)
fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            active=1,
            x=0.5,
            y=1.2,
            buttons=list([
                dict(label="City",
                     method="update",
                     args=[{"visible": [True] * len(df['City'].unique()) + [False] * len(df['County'].unique())}, 
                           {"title": "Vehicles in each City"}]),
                dict(label="County",
                     method="update",
                     args=[{"visible": [False] * len(df['City'].unique()) + [True] * len(df['County'].unique())}, 
                           {"title": "Vehicles in each County"}])
 
            ]),
        )
    ]
)

# Karten ausgabe
fig.show()
