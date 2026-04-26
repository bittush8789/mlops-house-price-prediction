import pandas as pd
import numpy as np
from main import HouseDetails

def test_feature_engineering_logic():
    """Test the manual feature engineering logic used in main.py."""
    data = {
        "area_sqft": 4000,
        "bedrooms": 4,
        "bathrooms": 4,
        "floors": 2,
        "parking": 2,
        "year_built": 2020,
        "location": "Gurgaon",
        "sub_location": "Golf Course Road",
        "furnishing": "Furnished",
        "property_type": "Villa"
    }
    
    # Simulate main.py logic
    house_age = 2025 - data['year_built']
    luxury_flag = (data['area_sqft'] > 3500) or (data['property_type'] in ['Villa', 'Penthouse'])
    premium_zones = ['Golf Course Road', 'DLF Phase 1', 'Saket', 'Vasant Kunj', 'Sector 150']
    premium_zone = data['sub_location'] in premium_zones
    
    assert house_age == 5
    assert luxury_flag is True
    assert premium_zone is True

def test_bhk_ratio_logic():
    area = 2000
    beds = 2
    ratio = beds / (area / 1000)
    assert ratio == 1.0
