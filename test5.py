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
years = df['Model Year'].unique()

# Layout der Dash-App definieren
app.layout = html.Div([
    html.Label("Wähle ein Jahr:"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': str(year), 'value': year} for year in years],
        value=years[0]
    ),
    html.Div(id='output-container')
])

# Callback-Funktion für die Aktualisierung der Ausgabe
@app.callback(
    Output('output-container', 'children'),
    [Input('year-dropdown', 'value')]
)
def update_output(selected_year):
    # Nach dem ausgewählten Jahr filtern
    filtered_data = df[df['Model Year'] == selected_year]

    # Anzahl der jeweils gleichen Auto-Modelle und -Makes zählen
    model_counts = filtered_data['Model'].value_counts().head(10)
    make_counts = filtered_data['Make'].value_counts().head(10)

    # Plotly Diagramme erstellen
    fig = go.Figure(data=[
        go.Bar(name='Model', x=model_counts.index, y=model_counts.values),
        go.Bar(name='Make', x=make_counts.index, y=make_counts.values)
    ])

    # Layout anpassen
    fig.update_layout(barmode='group', title=f'Top 10 Modelle und Makes im Jahr {selected_year}', xaxis_title='Modelle und Makes', yaxis_title='Anzahl')

    # Diagramm in Dash-Komponente umwandeln und zurückgeben
    return dcc.Graph(figure=fig)

# Dash-App starten
if __name__ == '__main__':
    app.run_server(debug=True)
