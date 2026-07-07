import pandas as pd

# Mock database simulating historical environmental data
# In a real scenario, this would be a query to a FAISS/ChromaDB vector store
# containing embedded satellite imagery or weather data.

mock_environmental_data = [
    {
        "region_id": "RS-101",
        "latitude_range": (26.0, 26.5),
        "longitude_range": (91.0, 91.5),
        "location": "Kamrup, Assam",
        "historical_data": "Severe flooding reported in July 2025. Crops heavily damaged due to waterlogging.",
        "soil_moisture_index": 0.85, # High moisture indicates flood
        "vegetation_health_index": 0.20 # Low health indicates damage
    },
    {
        "region_id": "RS-102",
        "latitude_range": (26.5, 27.0),
        "longitude_range": (92.0, 92.5),
        "location": "Sonitpur, Assam",
        "historical_data": "Drought conditions prevailing from May to August 2025. Rainfall 40% below average.",
        "soil_moisture_index": 0.15, # Low moisture indicates drought
        "vegetation_health_index": 0.30
    },
    {
        "region_id": "RS-103",
        "latitude_range": (27.0, 27.5),
        "longitude_range": (94.0, 94.5),
        "location": "Jorhat, Assam",
        "historical_data": "Normal weather patterns in 2025. Minor pest infestation reported in isolated patches, but overall yield normal.",
        "soil_moisture_index": 0.50, # Normal
        "vegetation_health_index": 0.85 # High health
    }
]

df_env = pd.DataFrame(mock_environmental_data)

def get_environmental_context(lat: float, lon: float) -> dict:
    """
    Simulates a similarity search or spatial query to retrieve environmental data
    based on latitude and longitude.
    """
    for index, row in df_env.iterrows():
        lat_min, lat_max = row["latitude_range"]
        lon_min, lon_max = row["longitude_range"]
        
        if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
            return {
                "location": row["location"],
                "historical_data": row["historical_data"],
                "soil_moisture_index": row["soil_moisture_index"],
                "vegetation_health_index": row["vegetation_health_index"]
            }
            
    # Default if coordinates don't match our mock regions
    return {
        "location": "Unknown Region",
        "historical_data": "No environmental records found for these coordinates in the database.",
        "soil_moisture_index": "N/A",
        "vegetation_health_index": "N/A"
    }
