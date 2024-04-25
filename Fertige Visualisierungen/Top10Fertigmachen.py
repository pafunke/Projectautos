import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output
import os

# Daten aus der CSV-Datei laden
csvDatei = 'cleaned_electric_cars_data_final.csv'
csv_path = os.path.join(os.path.dirname(__file__), csvDatei)
df = pd.read_csv(csv_path)

# Dash-App initialisieren
app = dash.Dash(__name__)

# Jahre aus der CSV-Datei extrahieren
min_year = df['Model Year'].min()
max_year = df['Model Year'].max()

# Layout der Dash-App definieren
app.layout = html.Div([
    html.Label("Wähle ein Jahr:"),
    dcc.Slider(
        id='year-slider',
        min=min_year,
        max=max_year,
        step=1,
        value=min_year,
        marks={year: str(year) for year in range(min_year, max_year+1)},
    ),
    html.Div([
        html.Div(dcc.Graph(id='model-graph'), style={'width': '50%', 'display': 'inline-block'}),
        html.Div(dcc.Graph(id='make-graph'), style={'width': '50%', 'display': 'inline-block'})
    ])
])

# Callback-Funktion für die Aktualisierung der Diagramme
@app.callback(
    [Output('model-graph', 'figure'),
     Output('make-graph', 'figure')],
    [Input('year-slider', 'value')]
)
def update_graphs(selected_year):
    # Nach dem ausgewählten Jahr filtern
    filtered_data = df[df['Model Year'] == selected_year]

    # Anzahl der jeweils gleichen Auto-Modelle und -Makes zählen
    model_counts = filtered_data['Model'].value_counts().head(10)
    make_counts = filtered_data['Make'].value_counts().head(10)

    # Plotly Diagramme für Modelle und Makes erstellen
    model_fig = go.Figure(go.Bar(x=model_counts.index, y=model_counts.values))
    model_fig.update_layout(title=f'Top 10 Modelle im Jahr {selected_year}', xaxis_title='Modelle', yaxis_title='Anzahl')

    make_fig = go.Figure(go.Bar(x=make_counts.index, y=make_counts.values))
    make_fig.update_layout(title=f'Top 10 Marken im Jahr {selected_year}', xaxis_title='Marken', yaxis_title='Anzahl')

    return model_fig, make_fig

# Dash-App starten
if __name__ == '__main__':
    app.run_server(debug=True)
