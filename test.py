import pandas as pd
import os

# Laden des Datensatzes
csvDatei = 'cleaned_electric_cars_data_final.csv'
csv_path = os.path.join(os.path.dirname(__file__), csvDatei)
df = pd.read_csv(csv_path)

# Anzeigen der ersten paar Zeilen des Datensatzes vor der Bereinigung

print(df.head())
