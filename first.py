from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import logging

# Initialize FastAPI app
app = FastAPI(title="Add,Sub,CtoF,FtoC")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app_operations.log"),
        logging.StreamHandler()
    ]
)

# Initialize HTTPBasic security
security = HTTPBasic()

# Mock user data
cred = {
    "user": {
        "username": "user",
        "password": "password"  # passwords
    }
}

# Function to authenticate user
def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = cred.get(credentials.username)
    if user is None or user['password'] != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return credentials.username

# Math Operations Router
math_root = APIRouter()

class MathInput(BaseModel):
    n1: float
    n2: float
    operation: str  # Operation can be '+' or '-'

@math_root.post("/calculate/")
def calculate(i: MathInput, username: str = Depends(authenticate_user)):
    try:
        if i.operation == "+":
            result = i.n1 + i.n2
            logging.info(f"Addition : {i.n1} + {i.n2} = {result}")
            return {"Result": result, "Operation": "Addition"}
        elif i.operation == "-":
            result = i.n1 - i.n2
            logging.info(f"Subtraction : {i.n1} - {i.n2} = {result}")
            return {"Result": result, "Operation": "Subtraction"}
        else:
            logging.warning(f"Invalid operation: {i.operation}")
            return {"Error": "Invalid operation. Please use '+' for addition or '-' for subtraction."}
    except Exception as e:
        logging.error(f"An error occurred in math operation: {str(e)}")
        return {"Error": "An unexpected error occurred in math operation."}

# --- Temperature Conversion Router ---
temp_root = APIRouter()

class TemperatureInput(BaseModel):
    value: float
    conversion: str  # Can be 'CtoF' or 'FtoC'

@temp_root.post("/convert/")
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

# --- Include Routers ---
app.include_router(math_root, prefix="/math",tags=["Math Operations"])
app.include_router(temp_root, prefix="/temperature",tags=["Temperature operations"])
