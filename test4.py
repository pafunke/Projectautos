import pandas as pd
import plotly.graph_objects as go
import os

# Daten aus der CSV-Datei laden
csvDatei = 'cleaned_electric_cars_data_final.csv'
csv_path = os.path.join(os.path.dirname(__file__), csvDatei)
df = pd.read_csv(csv_path)

# Nach Model Year filtern
filtered_data = df[df['Model Year'] == 2020]

# Anzahl der jeweils gleichen Auto-Modelle zählen
model_counts = filtered_data['Model'].value_counts()

# Anzahl der jeweils gleichen Auto-Makes zählen
make_counts = filtered_data['Make'].value_counts()

# Top 10 Modelle und Makes auswählen
top_10_models = model_counts.head(10)
top_10_makes = make_counts.head(10)

# Plotly Diagramme erstellen
fig = go.Figure(data=[
    go.Bar(name='Model', x=top_10_models.index, y=top_10_models.values),
    go.Bar(name='Make', x=top_10_makes.index, y=top_10_makes.values)
])

# Layout anpassen
fig.update_layout(barmode='group', title='Top 10 Modelle und Makes', xaxis_title='Modelle und Makes', yaxis_title='Anzahl')

# Diagramm anzeigen
fig.show()
