from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
import os

app = FastAPI(title="EstateAI - Production Valuation Engine")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

class HouseDetails(BaseModel):
    area_sqft: int
    bedrooms: int
    bathrooms: int
    floors: int
    parking: int
    year_built: int
    location: str
    sub_location: str
    furnishing: str
    property_type: str

# Load the optimized model
model_path = 'model/house_model.pkl'
try:
    model = joblib.load(model_path)
except Exception as e:
    model = None
    print(f"CRITICAL ERROR: {model_path} not found.")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/predict")
async def predict(details: HouseDetails):
    if model is None:
        raise HTTPException(status_code=500, detail="Production Model not loaded.")
    
    try:
        data = details.model_dump()
        
        # Advanced Feature Engineering (Sync with train_optimized.py)
        data['house_age'] = 2025 - data['year_built']
        data['total_rooms'] = data['bedrooms'] + data['bathrooms']
        data['bhk_to_area_ratio'] = data['bedrooms'] / (data['area_sqft'] / 1000)
        data['bath_per_bed'] = data['bathrooms'] / (data['bedrooms'] + 0.1)
        data['luxury_flag'] = (data['area_sqft'] > 3500) or (data['property_type'] in ['Villa', 'Penthouse'])
        
        premium_zones = ['Golf Course Road', 'DLF Phase 1', 'Saket', 'Vasant Kunj', 'Sector 150']
        data['premium_zone'] = data['sub_location'] in premium_zones
        
        input_df = pd.DataFrame([data])
        
        # Inference (Log-space)
        log_prediction = model.predict(input_df)[0]
        prediction = np.expm1(log_prediction)
        
        # Market Intelligence Logic
        price_per_sqft = prediction / data['area_sqft']
        
        # Tier Determination
        if prediction > 50000000: tier = "Ultra Luxury"
        elif prediction > 20000000: tier = "Premium"
        elif prediction > 8000000: tier = "Mid-Market"
        else: tier = "Budget"
        
        # AI Factors Simulation (SHAP-like)
        factors = []
        if data['premium_zone']: factors.append(f"Premium Location ({data['sub_location']}) +30%")
        if data['luxury_flag']: factors.append(f"Luxury Asset Class ({data['property_type']}) +25%")
        if data['house_age'] < 5: factors.append("New Construction Premium +10%")
        if not factors: factors.append("Standard Market Factors")
        
        # Confidence Logic
        confidence = "High" if data['area_sqft'] < 5000 else "Medium"
        
        return {
            "predicted_price": "₹{:,.0f}".format(prediction),
            "price_range": "₹{:,.0f} - ₹{:,.0f}".format(prediction * 0.96, prediction * 1.04),
            "market_tier": tier,
            "confidence_level": confidence,
            "price_per_sqft": "₹{:,.0f}/sqft".format(price_per_sqft),
            "ai_factors": " | ".join(factors)
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
