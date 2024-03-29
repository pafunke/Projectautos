import pandas as pd
import numpy
import os

# Load the dataset
df = pd.read_csv(os.path.join(os.path.dirname(__file__), '/Users/patrickfunke/src/DataVisulization/Project/data/Electric_Vehicle_Population_Data.csv'), sep=',')


# Display the first few rows of the dataset
print("Before cleaning:")
print(df.head())

# Drop irrelevant columns (if any)
df = df.drop(columns=['VIN (1-10)'])  # Example: Dropping 'VIN'
df = df.drop(columns=['DOL Vehicle ID']) 

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
    
    # Check if there are missing values for 'Reichweite' and 'MSRP'
    missingRange = same_model_rows['Electric Range'].isnull().all()
    missing_msrp = same_model_rows['Base MSRP'].isnull().all()
    
    if not missingRange or not missing_msrp:
        # Fill missing values with values from other rows with the same model
        if not missingRange:
            reichweite_value = same_model_rows['Electric Range'].dropna().iloc[0]
            df.loc[df['Model'] == model, 'Electric Range'] = reichweite_value
        
        if not missing_msrp:
            msrp_value = same_model_rows['Base MSRP'].dropna().iloc[0]
            df.loc[df['Model'] == model, 'Base MSRP'] = msrp_value

df['laengengrad'] = df['Vehicle location'].str.extract(r'POINT \(([^ ]+)').astype(float)
df['breitengrad'] = df['Vehicle location'].str.extract(r' ([^ ]+)\)').astype(float)



# Drop the original 'Vehicle location' column if no longer needed
df.drop(columns=['Vehicle location'], inplace=True)

# Display the first few rows of the dataset with longitude and latitude columns
print(df.head())

# Display the first few rows of the cleaned dataset
print("\nAfter cleaning:")
print(df.head())

# Save the cleaned dataset to a new CSV file
df.to_csv('cleaned_electric_cars_data.csv', index=False)
