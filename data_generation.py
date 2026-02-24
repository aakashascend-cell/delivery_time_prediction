import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

# Set seed for reproducibility
np.random.seed(42)

# Generate 10,000 orders
n_orders = 10000

# Amsterdam coordinates (center)
AMS_LAT, AMS_LON = 52.3676, 4.9041

# Generate data
data = []

for i in range(n_orders):
    # Order ID
    order_id = f"ORD{str(i+1).zfill(6)}"
    
    # Random datetime (Jan-Mar 2026)
    start_date = datetime(2026, 1, 1)
    random_days = np.random.randint(0, 90)
    random_hours = np.random.randint(10, 23)  # 10 AM - 11 PM
    random_mins = np.random.randint(0, 60)
    order_datetime = start_date + timedelta(days=random_days, hours=random_hours, minutes=random_mins)
    
    # Restaurant location (within Amsterdam)
    restaurant_lat = AMS_LAT + np.random.uniform(-0.05, 0.05)
    restaurant_lon = AMS_LON + np.random.uniform(-0.05, 0.05)
    
    # Customer location (within 10km of restaurant)
    customer_lat = restaurant_lat + np.random.uniform(-0.09, 0.09)
    customer_lon = restaurant_lon + np.random.uniform(-0.09, 0.09)
    
    # Calculate distance (approximate)
    lat_diff = (customer_lat - restaurant_lat) * 111  # km
    lon_diff = (customer_lon - restaurant_lon) * 111 * np.cos(np.radians(restaurant_lat))
    distance_km = np.sqrt(lat_diff**2 + lon_diff**2)
    
    # Order details
    num_items = np.random.randint(1, 8)
    order_value = round(num_items * np.random.uniform(8, 25), 2)
    
    # Time features
    day_of_week = order_datetime.strftime('%A')
    hour = order_datetime.hour
    is_weekend = day_of_week in ['Saturday', 'Sunday']
    
    # Weather (biased towards sunny)
    weather = np.random.choice(['sunny', 'rainy', 'snowy'], p=[0.6, 0.3, 0.1])
    
    # Traffic level (higher during rush hours)
    if hour in [12, 13, 18, 19, 20]:
        traffic_level = np.random.choice(['low', 'medium', 'high'], p=[0.1, 0.3, 0.6])
    else:
        traffic_level = np.random.choice(['low', 'medium', 'high'], p=[0.5, 0.3, 0.2])
    
    # Calculate delivery time
    base_time = distance_km * 3  # 3 min per km
    
    # Weather impact
    if weather == 'rainy':
        base_time += 8
    elif weather == 'snowy':
        base_time += 15
    
    # Traffic impact
    if traffic_level == 'high':
        base_time += 12
    elif traffic_level == 'medium':
        base_time += 5
    
    # Restaurant prep time (varies by hour and items)
    prep_time = 10 + (num_items * 2)
    if hour in [12, 13, 18, 19, 20]:
        prep_time += 5  # Busier = slower prep
    
    # Total time with noise
    actual_delivery_time = int(base_time + prep_time + np.random.uniform(-5, 8))
    actual_delivery_time = max(15, actual_delivery_time)  # Minimum 15 mins
    
    # Append row
    data.append({
        'order_id': order_id,
        'order_datetime': order_datetime,
        'restaurant_lat': round(restaurant_lat, 6),
        'restaurant_lon': round(restaurant_lon, 6),
        'customer_lat': round(customer_lat, 6),
        'customer_lon': round(customer_lon, 6),
        'num_items': num_items,
        'order_value': order_value,
        'day_of_week': day_of_week,
        'hour': hour,
        'is_weekend': is_weekend,
        'weather': weather,
        'traffic_level': traffic_level,
        'distance_km': round(distance_km, 2),
        'actual_delivery_time_minutes': actual_delivery_time
    })

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv(f'{Path.cwd()}/data/raw/delivery_data.csv', index=False)

print(f"✅ Generated {len(df)} orders")
print(f"\nFirst 5 rows:")
print(df.head())
print(f"\nBasic stats:")
print(df.describe())