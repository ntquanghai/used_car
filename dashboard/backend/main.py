from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import vehicles, stats, shap, performance
import uvicorn

app = FastAPI()
router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(vehicles.router)
app.include_router(stats.router)
app.include_router(shap.router)
app.include_router(performance.router)

if __name__ == "__main__":
    # Pass the application as an import string or the application object itself
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
