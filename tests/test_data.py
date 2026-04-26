import pandas as pd
import pytest
import os

def test_data_schema():
    """Validate the schema of the raw dataset."""
    df = pd.read_csv('data/raw.csv')
    expected_columns = [
        'area_sqft', 'bedrooms', 'bathrooms', 'floors', 'parking', 
        'year_built', 'location', 'sub_location', 'furnishing', 
        'property_type', 'price'
    ]
    for col in expected_columns:
        assert col in df.columns, f"Missing column: {col}"

def test_data_types():
    """Ensure data types are correct."""
    df = pd.read_csv('data/raw.csv')
    assert df['area_sqft'].dtype in ['int64', 'float64']
    assert df['price'].dtype in ['int64', 'float64']
    assert df['location'].dtype == 'object'
