from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import random
import uvicorn
import string
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"message": "Health Check Success!"}

# Path to the JSON file containing coupons
COUPON_FILE = "coupons.json"

# Helper function to load coupons from the JSON file
def load_coupons() -> List[str]:
    try:
        with open(COUPON_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Coupon file not found.")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding the coupon file.")

# Helper function to save updated coupon list to the JSON file
def save_coupons(coupons: List[str]):
    with open(COUPON_FILE, "w") as file:
        json.dump(coupons, file)

@app.get("/get-coupon/")
async def get_coupon():
    coupons = load_coupons()
    
    if len(coupons) == 0:
        raise HTTPException(status_code=404, detail="No coupons available")
    
    # Randomly select a coupon and remove it from the list
    selected_coupon = random.choice(coupons)
    coupons.remove(selected_coupon)
    
    # Save the updated coupon list back to the JSON file
    save_coupons(coupons)
    
    return {"coupon_code": selected_coupon, "remaining_coupons": len(coupons)}

# Endpoint to check remaining coupons
@app.get("/remaining-coupons/")
async def remaining_coupons():
    coupons = load_coupons()
    return {"remaining_coupons": len(coupons)}


def generate_random_coupon():
    random_part = ''.join(random.choices(string.digits, k=5))
    return f"COUPON{random_part}"

class CouponRequest(BaseModel):
    amount: int

@app.post("/add-coupon/")
async def add_coupon(body: CouponRequest):
    if body.amount is None or body.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0.")

    coupons = load_coupons()
    new_coupons = []

    for _ in range(body.amount):
        new_coupon = generate_random_coupon() 
        new_coupons.append(new_coupon)  
    
    coupons.extend(new_coupons) 

    save_coupons(coupons)

    return {"message": "Add coupon successful!"}
