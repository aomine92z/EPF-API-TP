import os
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import json
from ..services.utils import save_json

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

def load_dataset(filename):
    # Determine the file extension
    _, extension = os.path.splitext(filename)

    # Define the save directory
    save_directory = "services/epf-flower-data-science/src/data"
    filepath = os.path.join(save_directory, filename)

    # Read the file based on the extension
    if extension.lower() == '.json':
        data = pd.read_json(filepath)
    elif extension.lower() == '.csv':
        data = pd.read_csv(filepath)
    else:
        raise ValueError(f"Unsupported file extension: {extension}")

    return data.to_json(orient='records')

def split_dataset(df):

    def save_train_and_test_datasets(train_data, test_data):
        save_json(train_data, 'train_data.json')
        save_json(test_data, 'test_data.json')

    df = pd.read_json(df)
    # Split the dataset into train and test
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['Species'])

    # Convert DataFrames to JSON format
    train_json = train_df.to_json(orient='records')
    test_json = test_df.to_json(orient='records')

    # Save the train and test datasets
    save_train_and_test_datasets(train_json, test_json)

    # Return a JSON with both train and test sets
    return {
        "train_dataset": train_json,
        "test_dataset": test_json
    }

def train_classification_model(train_df):

    # Load model parameters from the JSON file
    with open('services/epf-flower-data-science/src/config/model_parameters.json', 'r') as file:
        parameters = json.load(file)

    train_df = pd.read_json(train_df)

    # Extract features and target variable
    X_train = train_df.drop(['Id','Species'], axis=1)
    y_train = train_df['Species']

    # Initialize the Random Forest Classifier with parameters
    model = RandomForestClassifier(**parameters)

    # Train the model
    model.fit(X_train, y_train)

    # Save the trained model to the src/models directory
    model_save_path = 'services/epf-flower-data-science/src/models/classification_model.joblib'
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    joblib.dump(model, model_save_path)

    return {"message": "Random Forest Classifier trained and saved successfully."}

def predict(test_df):

    # Load the saved model
    model = joblib.load('services/epf-flower-data-science/src/models/classification_model.joblib')  

    # Create a DataFrame from the input data
    test_df = pd.read_json(test_df)
    print(test_df.drop(['Id','Species'], axis=1))
    # Make predictions using the loaded model
    predictions = model.predict(test_df.drop(['Id','Species'], axis=1))

    # Create a list of dictionaries with predictions and IDs
    result_list = [{"prediction": str(prediction), "ID": int(identifier)} for prediction, identifier in zip(predictions.tolist(), test_df['Id'].tolist())]

    # Return the predictions as JSON
    return {"results": result_list}