import pandas as pd
import numpy as np
import os

def generate_production_data(n_rows=55000):
    np.random.seed(42)
    
    # Micro-locations and their base rates
    sub_locations = {
        'Delhi': {
            'Saket': 18000, 'Dwarka': 11000, 'Rohini': 9500, 
            'Vasant Kunj': 22000, 'Lajpat Nagar': 20000, 'Karol Bagh': 15000
        },
        'Gurgaon': {
            'DLF Phase 1': 25000, 'Golf Course Road': 35000, 'Sohna Road': 12000, 
            'Sector 56': 14000, 'New Gurgaon': 9000
        },
        'Noida': {
            'Sector 50': 10000, 'Sector 76': 8500, 'Sector 137': 7500, 'Sector 150': 9500
        },
        'Ghaziabad': {
            'Indirapuram': 6500, 'Vaishali': 7000, 'Raj Nagar Extension': 4500
        },
        'Faridabad': {
            'Sector 15': 6000, 'Green Valley': 5500, 'Neharpar': 4000
        }
    }
    
    cities = list(sub_locations.keys())
    property_types = ['Apartment', 'Villa', 'Builder Floor', 'Penthouse']
    furnishing_types = ['Furnished', 'Semi-Furnished', 'Unfurnished']
    
    data = []
    
    while len(data) < n_rows:
        city = np.random.choice(cities)
        sub_loc = np.random.choice(list(sub_locations[city].keys()))
        base_rate = sub_locations[city][sub_loc]
        
        area = np.random.randint(300, 7000)
        
        # Intelligent Constraints
        if area < 500:
            bedrooms = 1
            bathrooms = 1
            prop_type = 'Apartment'
        elif area < 1000:
            bedrooms = np.random.randint(1, 3)
            bathrooms = np.random.randint(1, 3)
            prop_type = np.random.choice(['Apartment', 'Builder Floor'])
        elif area > 3500:
            bedrooms = np.random.randint(4, 7)
            bathrooms = np.random.randint(4, 7)
            prop_type = np.random.choice(['Villa', 'Penthouse'])
        else:
            bedrooms = np.random.randint(2, 5)
            bathrooms = np.random.randint(2, 5)
            prop_type = np.random.choice(property_types)
            
        # Realistic combinations
        if prop_type == 'Penthouse' and area < 1800: continue
        if prop_type == 'Villa' and area < 1500: continue
        
        furnishing = np.random.choice(furnishing_types)
        floors = np.random.randint(1, 40) if prop_type == 'Apartment' else np.random.randint(1, 5)
        parking = np.random.randint(0, 5)
        year_built = np.random.randint(1990, 2026)
        age = 2025 - year_built
        
        # Advanced Pricing Engine
        price = area * base_rate
        
        # Premiums
        price += bedrooms * 600000
        price += bathrooms * 350000
        price += parking * 500000
        
        # Builder Reputation (Simulated)
        reputation_score = np.random.randint(1, 6)
        price *= (1 + (reputation_score * 0.05))
        
        if furnishing == 'Furnished': price *= 1.12
        if prop_type == 'Villa': price *= 1.45
        if prop_type == 'Penthouse': price *= 1.35
        
        # Luxury non-linear multipliers
        if area > 4000: price *= 1.3
        if city == 'Gurgaon' and base_rate > 20000: price *= 1.25 # Premium Zone
        
        # Depreciation
        price -= (age * 0.008 * price)
        if age > 25: price *= 0.8
        
        # Market Noise
        noise = np.random.uniform(0.92, 1.08)
        price *= noise
        
        data.append([
            area, bedrooms, bathrooms, floors, parking, 
            year_built, city, sub_loc, furnishing, prop_type, int(price)
        ])
        
    df = pd.DataFrame(data, columns=[
        'area_sqft', 'bedrooms', 'bathrooms', 'floors', 'parking', 
        'year_built', 'location', 'sub_location', 'furnishing', 'property_type', 'price'
    ])
    
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/house_data.csv', index=False)
    print(f"Generated {len(df)} rows of premium production data.")

if __name__ == "__main__":
    generate_production_data()
