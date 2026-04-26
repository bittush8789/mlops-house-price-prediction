import joblib
import os
import numpy as np
import pandas as pd

def test_model_loading():
    """Ensure the model file exists and can be loaded."""
    model_path = 'model/house_model.pkl'
    assert os.path.exists(model_path)
    model = joblib.load(model_path)
    assert model is not None

def test_model_inference():
    """Test if the model produces a valid numerical output."""
    model = joblib.load('model/house_model.pkl')
    
    # Create a dummy input matching the schema
    dummy_input = pd.DataFrame([{
        'area_sqft': 2000,
        'bedrooms': 3,
        'bathrooms': 2,
        'floors': 1,
        'parking': 1,
        'year_built': 2010,
        'location': 'Delhi',
        'sub_location': 'Saket',
        'furnishing': 'Furnished',
        'property_type': 'Apartment',
        'house_age': 15,
        'total_rooms': 5,
        'bhk_to_area_ratio': 1.5,
        'bath_per_bed': 0.66,
        'luxury_flag': False,
        'premium_zone': True
    }])
    
    prediction = model.predict(dummy_input)
    assert isinstance(prediction[0], (float, np.float32, np.float64))
    assert prediction[0] > 0
