import uvicorn
import fastapi

from src.app import get_application

app = get_application()

# Add a new endpoint for root redirection
@app.get("/", include_in_schema=False)
def root():
    return fastapi.responses.RedirectResponse('/docs')

if __name__ == "__main__":
    uvicorn.run("main:app", debug=True, reload=True, port=8080)
