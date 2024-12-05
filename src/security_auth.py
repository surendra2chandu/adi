
from fastapi import FastAPI,APIRouter,Depends,HTTPException
from fastapi.security import HTTPBasic,HTTPBasicCredentials
import logging

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