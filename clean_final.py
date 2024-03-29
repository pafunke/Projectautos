import pandas as pd
import os

# Laden des Datensatzes
df = pd.read_csv(os.path.join(os.path.dirname(__file__), '/Users/patrickfunke/src/DataVisulization/Project/data/Electric_Vehicle_Population_Data.csv'), sep=',')

# Anzeigen der ersten paar Zeilen des Datensatzes
print("Vor der Bereinigung:")
print(df.head())

# Löschen irrelevanter Spalten (falls vorhanden)
df.rename(columns={'VIN (1-10)': 'VIN'}, inplace=True)

# fehlende werte raus + spaltennamen als Variablen +  nur kleinbuchstaben
df = df.dropna() # eigentlich unnötig
categorical_columns = ['County', 'City', 'State', 'Make', 'Model', 'Electric Vehicle Type']
df[categorical_columns] = df[categorical_columns].apply(lambda x: x.str.lower())
df[categorical_columns] = df[categorical_columns].applymap(lambda x: x.strip() if isinstance(x, str) else x)


#Katasstrophe:

modelData = {}
#preis + range speichern wenn != 0
for index, row in df.iterrows():
    model = row['Model']
    price = row['Base MSRP']
    range = row['Electric Range']
    
    if model not in modelData:
        modelData[model] = {'price': None, 'range': None}
    if pd.notna(price) and price != 0:  
        modelData[model]['price'] = price
    if pd.notna(range) and range != 0:  
        modelData[model]['range'] = range

for index, row in df.iterrows():
    model = row['Model']
    
    # wenn 0 dann  gespeicherten wert eintragen 
    if pd.isna(row['Base MSRP']) or row['Base MSRP'] == 0: 
        df.at[index, 'Base MSRP'] = modelData[model]['price']
    if pd.isna(row['Electric Range']) or row['Electric Range'] == 0:
        df.at[index, 'Electric Range'] = modelData[model]['range']


# ['Vehicle Location'] in längen und breitengrad umwandeln
# Point = The center of the ZIP Code for the registered vehicle.
df['laengengrad'] = df['Vehicle Location'].str.extract(r'POINT \(([^ ]+)').astype(float)
df['breitengrad'] = df['Vehicle Location'].str.extract(r' ([^ ]+)\)').astype(float)
#Alte spalte löschen
df.drop(columns=['Vehicle Location'], inplace=True)


print(df.head())

# Speichern des bereinigten Datensatzes
df.to_csv('cleaned_electric_cars_data_final.csv', index=False)
