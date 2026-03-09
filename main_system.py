import joblib
import sqlite3
import random

# 1. Load the "Brain" we created in Step 1
model = joblib.load('tilapia_model.pkl')

def get_simulated_sensor_data():
    # Mimicking the ESP32 sensors in MacArthur, Leyte
    return {
        'ph': round(random.uniform(5.0, 9.0), 2),
        'temp': round(random.uniform(22.0, 32.0), 2),
        'do': round(random.uniform(2.0, 8.0), 2),
        'turbidity': round(random.uniform(5.0, 50.0), 2)
    }

def run_feeding_logic():
    # Connect to the Warehouse
    conn = sqlite3.connect('aquaculture.db')
    cursor = conn.cursor()
    
    # Get sensor readings
    sensors = get_simulated_sensor_data()
    
    # ML Prediction: [pH, Temp, DO, Turbidity]
    input_data = [[sensors['ph'], sensors['temp'], sensors['do'], sensors['turbidity']]]
    quality = int(model.predict(input_data)[0])
    
    # Feeding Heuristics (From your Math Model)
    # 2=Good (Feed 110%), 1=Avg (Feed 70%), 0=Bad (Stop)
    feed_status = "FULL" if quality == 2 else "REDUCED" if quality == 1 else "STOPPED"
    
    # Save to Database
    cursor.execute('''
        INSERT INTO SensorLogs (device_id, ph, temp, do, turbidity, quality_score)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("PI_LEYTE_01", sensors['ph'], sensors['temp'], sensors['do'], sensors['turbidity'], quality))
    
    conn.commit()
    conn.close()
    
    print(f"--- Pond Update ---")
    print(f"Sensors: {sensors}")
    print(f"Quality Score: {quality} | Feeding Action: {feed_status}")

    # Constants for your MacArthur, Leyte setup
NUMBER_OF_FISH = 500
AVERAGE_WEIGHT_GRAMS = 250 # 250g per fish
FEED_RATE = 0.03 # Tilapia eat ~3% of body weight daily

def calculate_feed_grams(quality_score):
    total_biomass = NUMBER_OF_FISH * AVERAGE_WEIGHT_GRAMS
    daily_base_feed = total_biomass * FEED_RATE
    
    # Apply the Math Model multipliers
    if quality_score == 2:   # Good
        return daily_base_feed * 1.1 / 3 # Divided by 3 meals a day
    elif quality_score == 1: # Average
        return daily_base_feed * 0.7 / 3
    else:                    # Bad
        return 0

# Run it once to test
run_feeding_logic()