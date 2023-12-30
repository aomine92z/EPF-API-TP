from fastapi import HTTPException, Depends, Request, APIRouter
from google.cloud import firestore
import json
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="services/epf-flower-data-science/src/templates")  # Specify the directory where your templates are stored

with open("services/epf-flower-data-science/iac/ga4-project-402308-ee5333701e7c.json") as json_file:
    # Initialisez le client Firestore avec la clé de service
    db = firestore.Client.from_service_account_info(
        info = json.load(json_file)
    )

# Step 13: Create the Firestore collection
collection_name = "parameters"
collection_ref = db.collection(collection_name)

@router.on_event("startup")
async def startup_event():
    # Ensure Firestore collection has at least one document on startup
    if collection_ref.stream():
        # Collection already has documents, no need to add default parameters
        return

    # Create the collection with default parameters if it doesn't exist
    collection_ref.add({"n_estimators": 100, "criterion": "gini"})

@router.get("/get_parameters")
async def get_parameters():
    # Step 14: Retrieve parameters from Firestore
    # Assuming you want to get a specific document, change the document ID accordingly
    parameters_doc = collection_ref.document("17sAXmC5Oru6QPuMXMLo").get()

    if parameters_doc.exists:
        # Extract the data from the document snapshot
        parameters = parameters_doc.to_dict()
        return {"parameters": parameters}
    else:
        raise HTTPException(status_code=404, detail="Parameters document not found")

@router.get("/update_parameters", response_class=HTMLResponse)
async def update_parameters_form(request: Request):
    # Retrieve current values from Firestore or your storage
    current_values = (await get_parameters()).get("parameters")

    return templates.TemplateResponse(
        "update_parameters.html",
        {"request": request, "current_values": current_values}
    )

@router.put("/update_parameters", response_class=HTMLResponse)
async def update_parameters(request: Request, n_estimators: int, criterion: str):
    # Validate input parameters
    if not n_estimators > 0:
        raise HTTPException(status_code=400, detail="Invalid value for n_estimators. It must be greater than 0.")

    valid_criteria = {"gini", "entropy"}  # Add other valid criteria as needed
    if criterion not in valid_criteria:
        raise HTTPException(status_code=400, detail=f"Invalid criterion. Valid criteria are {valid_criteria}")

    # Your Firestore update logic
    collection_ref.document("17sAXmC5Oru6QPuMXMLo").set({"n_estimators": n_estimators, "criterion": criterion}, merge=True)

    return templates.TemplateResponse(
        "update_parameters.html",
        {"request": request, "current_values": {"n_estimators": n_estimators, "criterion": criterion}}
    )