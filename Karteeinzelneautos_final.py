import pandas as pd
import plotly.graph_objs as go

# Lesen der Daten
df = pd.read_csv('/Users/patrickfunke/CodeHub/Projectautos/data/cleaned_electric_cars_data_final.csv')

# Funktion zum Erstellen des Karteninhalts
def create_map_data(df, location_type=None, location=None, show_count=False):
    # Filtern nach 'County' und 'City', je nach Auswahl
    if location_type == 'County':
        df = df[df['County'] == location]
    elif location_type == 'City':
        df = df[df['City'] == location]

    data = []
    if show_count:
        count_df = df.groupby(['City']).size().reset_index(name='count')
        for index, row in count_df.iterrows():
            city = row['City']
            count = row['count']
            data.append(go.Scattermapbox(
                lat=df[df['City'] == city]['breitengrad'],
                lon=df[df['City'] == city]['laengengrad'],
                mode='markers',
                marker=dict(
                    size=count * 3,
                    color='blue',
                    opacity=0.7,
                ),
                text=f'{city}: {count} vehicles',
                name=city
            ))
    else:
        data.append(go.Scattermapbox(
            lat=df['breitengrad'],
            lon=df['laengengrad'],
            mode='markers',
            marker=dict(
                size=8,
                color='blue',
                opacity=0.7,
            ),
            text=df[['Model', 'Make', 'Electric Vehicle Type']].astype(str),
            name='All Vehicles'
        ))

    return data

mapboxLayout = {
    'accesstoken': 'pk.eyJ1Ijoid2kyMzA0NCIsImEiOiJjbHUzNnhkN3AweGY5Mm1ueHlhaWl0YXdtIn0.1nuiwQqcap38GeVekTrj0A',
    'center': {'lat': df['breitengrad'].mean(), 'lon': df['laengengrad'].mean()},
    'zoom': 6.2
}

# Layout der Karte konfigurieren
layout = go.Layout(mapbox=mapboxLayout)

# Karte erstellen
fig = go.Figure(layout=layout)

# Karteninhalt erstellen (zeigt zuerst alle Fahrzeuge)
data = create_map_data(df)

# Daten zur Karte hinzufügen
for trace in data:
    fig.add_trace(trace)

# Funktion für Knopfaktionen
def update_map(location_type, location):
    fig.data = []
    if location_type and location:
        data = create_map_data(df, location_type, location, show_count=True)
    else:
        data = create_map_data(df)
    for trace in data:
        fig.add_trace(trace)

# Knöpfe für die Auswahl des Kartentyps erstellen
buttons = [
    dict(label='Alle Fahrzeuge', method='update', args=[{'visible': True}, {}]),
    dict(label='Fahrzeuganzahl in Stadt', method='update', args=[{'visible': True}, {'location_type': 'City', 'location': 'Seattle'}]),
    dict(label='Fahrzeuganzahl im County', method='update', args=[{'visible': True}, {'location_type': 'County', 'location': 'Los Angeles County'}])
]

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

# Knöpfe den Aktionen zuordnen
for button in buttons:
    button['args'][0]['visible'] = [False] * len(fig.data)
    button['args'][0]['visible'][0] = True

fig.show()
