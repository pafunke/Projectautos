import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output
import os

dashvar = dash.Dash(__name__)

# Daten aus der CSV-Datei laden
csvDatei = 'cleaned_electric_cars_data_final.csv'
csv_path = os.path.join(os.path.dirname(__file__), csvDatei)
df = pd.read_csv(csv_path)

# Dynamisch die Jahre -> Damit code weiter auf neue Einträge reagieren könnte 19 - 20024
min_year = df['Model Year'].min()
max_year = df['Model Year'].max()

# Layout
dashvar.layout = html.Div([
    html.Label("Wähle ein Jahr:"),
    dcc.Slider(
        id='year-slider',
        min=min_year,
        max=max_year,
        step=1,
        value=min_year,
        marks={year: str(year) for year in range(min_year, max_year + 1)},included=False
    ),
    html.Div([
        html.Div(dcc.Graph(id='model-graph'), 
                 style={'width': '50%', 'display': 'inline-block'}),
        html.Div(dcc.Graph(id='make-graph'), 
                 style={'width': '50%', 'display': 'inline-block'}),
        html.Div(dcc.Graph(id='time-series-graph'), 
                 style={'width': '100%', 'display': 'inline-block'})
    ]),
])

# Funktion zur Bestimmung der Balkenfarbe basierend auf dem Fahrzeugtyp
def get_color(ev_type):
    if ev_type.lower() == 'battery electric vehicle (bev)':
        return 'lightgreen'
    elif ev_type.lower() == 'plug-in hybrid electric vehicle (phev)':
        return 'lightblue'
    else:
        return 'grey'  #falls falsche daten dürften aber keine sein


@dashvar.callback(
    [Output('model-graph', 'figure'),
     Output('make-graph', 'figure'),
     Output('time-series-graph', 'figure')],
    [Input('year-slider', 'value')]
)
def update_graphs(selected_year):
    # Daten nach Jahr filtern
    filtered_data = df[df['Model Year'] == selected_year]

    # Value Counts für Top 10 Modelle und Marken
    modelAnzahl = filtered_data['Model'].value_counts().head(10)
    makeAnzahl = filtered_data['Make'].value_counts().head(10)

    # Diagramm für Top 10 Modelle erstellen
    model_fig = go.Figure(go.Bar(
        x=modelAnzahl.index,
        y=modelAnzahl.values,
        marker_color=[get_color(ev_type) for ev_type in filtered_data.groupby('Model')['Electric Vehicle Type'].first().loc[modelAnzahl.index]]
    ))
    model_fig.update_layout(title=f'Top 10 Modelle im Jahr {selected_year}', 
                            xaxis_title='Modelle: Grün: Elektrisch | Blau: Hybride', 
                            yaxis_title='Anzahl')

    # Diagramm für Top 10 Marken 
    make_fig = go.Figure(go.Bar(
        x=makeAnzahl.index,
        y=makeAnzahl.values,
        #marker_color='blue'  #standard sieht besser aus
    ))
    make_fig.update_layout(title=f'Top 10 Marken im Jahr {selected_year}', 
                           xaxis_title='Marken', 
                           yaxis_title='Anzahl')

    # Zeitverlaufskurve für Elektroautos und Hybriden
    elektroLinienDaten = df.groupby(['Model Year', 'Electric Vehicle Type']).size().unstack().fillna(0)
    elktroFarbe = 'lightgreen'
    hybridFarbe = 'lightblue'
    time_series_fig = go.Figure()
    for column in elektroLinienDaten.columns:
        if column == 'battery electric vehicle (bev)':  # Elektroautos (BEV)
            color = elktroFarbe
        elif column == 'plug-in hybrid electric vehicle (phev)':  # Hybride
            color = hybridFarbe
        else :
            color='gray'

        time_series_fig.add_trace(go.Scatter(x=elektroLinienDaten.index, 
                                             y=elektroLinienDaten[column], 
                                             mode='lines', 
                                             name=column,
                                             line=dict(color=color),

                                             ))


    time_series_fig.update_layout(title='Zeitverlauf von Elektroautos und Hybriden',
                                  xaxis_title='Jahr', 
                                  yaxis_title='Anzahl',
                                xaxis=dict(tickvals=list(range(min(elektroLinienDaten.index), 
                                                                            max(elektroLinienDaten.index) , 1)),
                                                                            range=[min(elektroLinienDaten.index), 
                                                                                   max(elektroLinienDaten.index)-1])                                  
                                  
                                  )

    return model_fig, make_fig, time_series_fig

# Dashbord 
if __name__ == '__main__':
    dashvar.run_server()
