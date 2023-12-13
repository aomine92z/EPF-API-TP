from fastapi import APIRouter, HTTPException
from src.services.data import download_dataset, load_dataset
from src.services.cleaning import clean_species_column

router = APIRouter()

@router.get("/download_data")
def download_data():
    return download_dataset()

@router.get("/load_data")
def load_data():
    try:
        data = load_dataset()
        return data
    
    # We return a specific HTTP status code and message
    except HTTPException as e:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # Alternatively, we return a generic 500 Internal Server Error
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
@router.get("/process_data")
def process_data():
    try:
        data = clean_species_column(load_data())
        return data
    
    # We return a specific HTTP status code and message
    except HTTPException as e:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # Alternatively, we return a generic 500 Internal Server Error
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

