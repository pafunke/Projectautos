import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Annahme: Die CSV-Datei heißt 'cleaned_electric_cars_data_final.csv'
csvDatei = 'cleaned_electric_cars_data_final.csv'
csv_path = os.path.join(os.path.dirname(__file__), csvDatei)
df = pd.read_csv(csv_path)

filtered_data = df[df['Model Year'] == 2020]

# Anzahl der jeweils gleichen Auto-Modelle zählen
model_counts = filtered_data['Model'].value_counts()

# Top 10 Modelle auswählen
top_10_models = model_counts.head(10)

# Anzahl der jeweils gleichen Auto-Makes zählen
make_counts = filtered_data['Make'].value_counts()

# Top 10 Makes auswählen
top_10_makes = make_counts.head(10)

print("Top 10 Modelle:")
print(top_10_models)

print("\nTop 10 Makes:")
print(top_10_makes)



# # Funktion zur Erstellung des interaktiven Balkendiagramms für die Top 10 Modelle
# def create_model_plot(year):
#     # Daten für das ausgewählte Jahr filtern
#     df_year = df[df['Model Year'].dt.year == year]
    
#     # Top 10 beliebteste Modelle für das ausgewählte Jahr ermitteln
#     top_models = df_year['Model'].value_counts().nlargest(10)
#     print(top_models)
#     # Plotting des Balkendiagramms für die Top 10 Modelle mit Plotly
#     fig = go.Figure(data=[go.Bar(x=top_models.values, y=top_models.index, orientation='h')])
#     fig.update_layout(title=f'Top 10 Modelle für das Jahr {year}',
#                       xaxis_title='Anzahl der Fahrzeuge',
#                       yaxis_title='Modelle',
#                       barmode='stack')
#     return fig

# # Funktion zur Erstellung des interaktiven Balkendiagramms für die Top 10 Marken
# def create_make_plot(year):
#     # Daten für das ausgewählte Jahr filtern
#     df_year = df[df['Model Year'].dt.year == year]
    
#     # Top 10 beliebteste Marken für das ausgewählte Jahr ermitteln
#     top_brands = df_year['Make'].value_counts().nlargest(10)
    
#     # Plotting des Balkendiagramms für die Top 10 Marken mit Plotly
#     fig = go.Figure(data=[go.Bar(x=top_brands.values, y=top_brands.index, orientation='h')])
#     fig.update_layout(title=f'Top 10 Marken für das Jahr {year}',
#                       xaxis_title='Anzahl der Fahrzeuge',
#                       yaxis_title='Marken',
#                       barmode='stack')
#     return fig

# # Beispielaufruf der Funktionen mit dem Jahr 2020
# model_plot = create_model_plot(2020)
# make_plot = create_make_plot(2020)

# # Die Diagramme nebeneinander platzieren
# fig = make_subplots(rows=1, cols=2)

# # Model-Plot links platzieren
# fig.add_trace(model_plot.data[0], row=1, col=1)
# fig.update_xaxes(title_text="Anzahl der Fahrzeuge", row=1, col=1)
# fig.update_yaxes(title_text="Modelle", row=1, col=1)

# # Marken-Plot rechts platzieren
# fig.add_trace(make_plot.data[0], row=1, col=2)
# fig.update_xaxes(title_text="Anzahl der Fahrzeuge", row=1, col=2)
# fig.update_yaxes(title_text="Marken", row=1, col=2)

# # Titel setzen
# fig.update_layout(title_text=f'Top 10 Modelle und Marken für das Jahr 2020')

# fig.show(renderer="browser")
