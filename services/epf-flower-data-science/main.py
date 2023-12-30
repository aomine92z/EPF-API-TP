import uvicorn
import fastapi
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.app import get_application

app = get_application()
templates = Jinja2Templates(directory="services/epf-flower-data-science/src/templates")

# Add a new endpoint for root redirection -- STEP 3 EXERCICE IN COMMENT FOR BETTER USABILITY OF THE APP
# @app.get("/", include_in_schema=False)
# def root():
#     return fastapi.responses.RedirectResponse('/docs')

@app.get("/", response_class=HTMLResponse)
def root(request: fastapi.Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("main:app", debug=True, reload=True, port=8080)
