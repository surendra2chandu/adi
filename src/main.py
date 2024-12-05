from fastapi import FastAPI
from src.math_root import router as math_router
from src.temp_root import router as temp_router
from fastapi import FastAPI, APIRouter, Depends, HTTPException

app = FastAPI()

# --- Include Routers ---
app.include_router(math_router)
app.include_router(temp_router)
