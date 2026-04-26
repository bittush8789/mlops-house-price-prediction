import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import StackingRegressor, RandomForestRegressor
from xgboost import XGBRegressor

def train_production_model():
    df = pd.read_csv('data/house_data.csv')
    
    # Feature Engineering
    df['house_age'] = 2025 - df['year_built']
    df['total_rooms'] = df['bedrooms'] + df['bathrooms']
    df['bhk_to_area_ratio'] = df['bedrooms'] / (df['area_sqft'] / 1000)
    df['bath_per_bed'] = df['bathrooms'] / (df['bedrooms'] + 0.1)
    df['luxury_flag'] = (df['area_sqft'] > 3500) | (df['property_type'].isin(['Villa', 'Penthouse']))
    
    premium_zones = ['Golf Course Road', 'DLF Phase 1', 'Saket', 'Vasant Kunj', 'Sector 150']
    df['premium_zone'] = df['sub_location'].isin(premium_zones)
    
    X = df.drop(['price'], axis=1)
    y = np.log1p(df['price'])
    
    cat_cols = ['location', 'sub_location', 'furnishing', 'property_type']
    num_cols = X.select_dtypes(include=[np.number]).columns.tolist()
    
    preprocessor = ColumnTransformer([
        ('num', StandardScaler(), num_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)
    ])
    
    estimators = [
        ('xgb', XGBRegressor(n_estimators=300, max_depth=8, learning_rate=0.05, random_state=42)),
        ('rf', RandomForestRegressor(n_estimators=200, max_depth=15, random_state=42))
    ]
    
    stacking = StackingRegressor(estimators=estimators, final_estimator=XGBRegressor())
    
    model_pipeline = Pipeline([
        ('pre', preprocessor),
        ('reg', stacking)
    ])
    
    model_pipeline.fit(X, y)
    
    os.makedirs('model', exist_ok=True)
    joblib.dump(model_pipeline, 'model/house_model.pkl')
    print("Production Stacking Model trained and saved.")

if __name__ == "__main__":
    train_production_model()
