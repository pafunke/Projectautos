import pandas as pd
import os

# Laden des Datensatzes
df = pd.read_csv(os.path.join(os.path.dirname(__file__), '/Users/patrickfunke/src/DataVisulization/Project/data/Electric_Vehicle_Population_Data.csv'), sep=',')

# Anzeigen der ersten paar Zeilen des Datensatzes
print("Vor der Bereinigung:")
print(df.head())

# Löschen irrelevanter Spalten (falls vorhanden)
df = df.drop(columns=['VIN (1-10)', 'DOL Vehicle ID'])

# Entfernen von Zeilen mit fehlenden Werten
df = df.dropna()

# Konvertieren kategorischer Spalten in Kleinbuchstaben
categorical_columns = ['County', 'City', 'State', 'Make', 'Model', 'Electric Vehicle Type']
df[categorical_columns] = df[categorical_columns].apply(lambda x: x.str.lower())

# Entfernen führender und nachfolgender Leerzeichen aus Zeichenfolgenspalten
df[categorical_columns] = df[categorical_columns].applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Iterieren über jedes Modell
for model in df['Model'].unique():
    # Finden von Zeilen mit demselben Modell
    same_model_rows = df[df['Model'] == model]
    
    # Überprüfen, ob Werte für 'Electric Range' und 'Base MSRP' fehlen
    missing_reichweite = same_model_rows['Electric Range'].isnull().all()
    missing_msrp = same_model_rows['Base MSRP'].isnull().all()
    
    if missing_reichweite or missing_msrp:  # Änderung der Bedingung
        # Fehlende Werte mit Werten aus anderen Zeilen desselben Modells füllen
        if not missing_reichweite:
            reichweite_value = same_model_rows['Electric Range'].dropna().iloc[0]
            df.loc[df['Model'] == model, 'Electric Range'] = reichweite_value
        
        if not missing_msrp:
            msrp_value = same_model_rows['Base MSRP'].dropna().iloc[0]
            df.loc[df['Model'] == model, 'Base MSRP'] = msrp_value


# Extrahieren von Längen- und Breitengrad aus der Spalte 'Vehicle Location'
df['laengengrad'] = df['Vehicle Location'].str.extract(r'POINT \(([^ ]+)').astype(float)
df['breitengrad'] = df['Vehicle Location'].str.extract(r' ([^ ]+)\)').astype(float)

# Löschen der Originalspalte 'Vehicle Location', falls nicht mehr benötigt
df.drop(columns=['Vehicle Location'], inplace=True)

# Anzeigen der ersten paar Zeilen des bereinigten Datensatzes
print("\nNach der Bereinigung:")
print(df.head())#
df.to_csv('cleaned_electric_cars_data2.csv', index=False)

