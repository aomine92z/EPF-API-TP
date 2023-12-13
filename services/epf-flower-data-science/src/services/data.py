import os
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

def download_dataset():
    # URL of the Iris dataset on Kaggle
    dataset_name = "uciml/iris"

    # Directory to save the dataset
    save_directory = "services/epf-flower-data-science/src/data"
    os.makedirs(save_directory, exist_ok=True)

    # Authenticate with Kaggle API
    api = KaggleApi()
    api.authenticate()

    # Download the dataset using Kaggle API
    api.dataset_download_files(dataset_name, path=save_directory, unzip=True)

    # For simplicity, return a success message
    return {"message": "Iris dataset downloaded and saved successfully."}

def load_dataset():
    try:
        filepath = 'C:/Users/Amine/Desktop/EPF-API-TP/services/epf-flower-data-science/src/data/Iris.csv'
        df = pd.read_csv(filepath)
        return df.to_json(orient='records')
    except FileNotFoundError:
        return {"error": "File not found. Make sure the dataset file exists at the specified path."}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}