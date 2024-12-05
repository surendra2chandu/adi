# --- Temperature Conversion Router ---

# import statements
from fastapi import FastAPI,APIRouter,Depends
from src.security_auth import authenticate_user
from pydantic import BaseModel

import logging


router = APIRouter(prefix="/temperature",tags=["Temperature operations"])

class TemperatureInput(BaseModel):
    value: float
    conversion: str  # Can be 'CtoF' or 'FtoC'

@router.post("/convert/")
def convert_temperature(data: TemperatureInput, username: str = Depends(authenticate_user)):
    try:
        if data.conversion == "CtoF":
            result = (data.value * 9/5) + 32
            logging.info(f"Converted {data.value}°C to {result}°F")
            return {"Input": f"{data.value}°C", "Converted": f"{result}°F"}
        elif data.conversion == "FtoC":
            result = (data.value - 32) * 5/9
            logging.info(f"Converted {data.value}°F to {result}°C")
            return {"Input": f"{data.value}°F", "Converted": f"{result}°C"}
        else:
            logging.warning(f"Invalid conversion type: {data.conversion}")
            return {"Error": "Invalid conversion type. Use 'CtoF' for Celsius to Fahrenheit or 'FtoC' for Fahrenheit to Celsius."}
    except Exception as e:
        logging.error(f"An error occurred in temperature conversion: {str(e)}")
        return {"Error": "An unexpected error occurred in temperature conversion. "}
