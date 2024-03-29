import pandas as pd
import os

# Laden des Datensatzes
df = pd.read_csv(os.path.join(os.path.dirname(__file__), '/Users/patrickfunke/src/DataVisulization/Project/data/Electric_Vehicle_Population_Data.csv'), sep=',')

# Anzeigen der ersten paar Zeilen des Datensatzes vor der Bereinigung
print("Vor der Bereinigung:")
print(df.head())

# Drop irrelevant columns (if any)
df = df.drop(columns=['VIN (1-10)', 'DOL Vehicle ID'])

# Remove any rows with missing values
df = df.dropna()

# Convert categorical columns to lowercase
categorical_columns = ['County', 'City', 'State', 'Make', 'Model', 'Electric Vehicle Type']
df[categorical_columns] = df[categorical_columns].apply(lambda x: x.str.lower())

# Remove leading and trailing whitespaces from string columns
df[categorical_columns] = df[categorical_columns].applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Iterate over each model
for model in df['Model'].unique():
    # Find rows with the same model
    same_model_rows = df[df['Model'] == model]
    
    # Check if there are missing values for 'Electric Range' and 'Base Base MSRP'
    missing_reichweite = same_model_rows['Electric Range'].isnull().all()
    missing_msrp = same_model_rows['Base MSRP'].isnull().all()
    
    if not missing_reichweite or not missing_msrp:
        # Fill missing values with values from other rows with the same model
        if not missing_reichweite:
            reichweite_value = same_model_rows['Electric Range'].dropna().iloc[0]
            df.loc[df['Model'] == model, 'Electric Range'] = reichweite_value
        
        if not missing_msrp:
            msrp_value = same_model_rows['Base MSRP'].dropna().iloc[0]
            df.loc[df['Model'] == model, 'Base MSRP'] = msrp_value

# Extrahiere Längen- und Breitengrad aus der Spalte 'Vehicle Location'
df['laengengrad'] = df['Vehicle Location'].str.extract(r'POINT \(([^ ]+)').astype(float)
df['breitengrad'] = df['Vehicle Location'].str.extract(r' ([^ ]+)\)').astype(float)

# Lösche die Originalspalte 'Vehicle Location', falls nicht mehr benötigt
df.drop(columns=['Vehicle Location'], inplace=True)

# Anzeigen der ersten paar Zeilen des bereinigten Datensatzes
print("\nNach der Bereinigung:")
print(df.head())

# Kopiere den DataFrame vor der Bereinigung
df_before = df.copy()

# Hinzufügen einer neuen Spalte, um die Änderungen in der Spalte 'Base Base MSRP' zu vergleichen
df['Base MSRP Change'] = df.groupby('Model')['Base MSRP'].diff()

# Filtern der Zeilen, in denen sich der 'Base Base MSRP' geändert hat
changed_rows = df[df['Base MSRP Change'].notnull()]

# Merge der DataFrames vor und nach der Bereinigung basierend auf dem Model
merged_df = pd.merge(changed_rows, df_before, on='Model', suffixes=('_neu', '_alt'))

# Auswahl nur relevanter Spalten und Anzeigen der Ergebnisse
result_df = merged_df[['Model', 'Base MSRP_alt', 'Base MSRP_neu']]
print("\nÄnderungen in der Spalte 'Base MSRP':")
print(result_df)
df.to_csv('spaltenVergleich.csv', index=False)
