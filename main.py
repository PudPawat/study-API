from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import random
from typing import List

app = FastAPI()

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
