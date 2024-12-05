# Math Operations Router

# Import statements
from fastapi import FastAPI,APIRouter,Depends
from src.security_auth import authenticate_user
from pydantic import BaseModel
import logging



router = APIRouter(prefix="/math",tags=["Math Operations"])

class MathInput(BaseModel):
    n1: float
    n2: float
    operation: str  # Operation can be '+' or '-'

@router.post("/calculate/")
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
