import pandas as pd

def clean_species_column(df):
    df = pd.read_json(df)
    # Check if the "Species" column exists in the DataFrame
    if 'Species' in df.columns:
        # Remove "Iris-" prefix and title the strings
        df['Species'] = df['Species'].str.replace('Iris-', '').str.title()

    return df.to_json(orient='records')