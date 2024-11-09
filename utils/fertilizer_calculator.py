# Importing plant and disease data from the plant_data module
import sys
import json
from utils.plant_data import plant_database, disease_adjustments
from typing import Optional, Dict
import os

# Add the project root directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Fertilizer calculator function
def get_fertilizer_recommendation(plant, growth_stage, disease=None, soil_data=None):
    """
    Calculate the fertilizer needs based on plant type, growth stage, disease, and soil data.
    
    Parameters:
        plant (str): Type of plant (e.g., "tomato", "wheat")
        growth_stage (str): Growth stage (e.g., "seedling", "flowering")
        disease (str, optional): Detected disease affecting the plant (e.g., "powdery_mildew")
        soil_data (dict, optional): Current soil nutrient levels for N, P, K (e.g., {"N": 8, "P": 12, "K": 9})
        
    Returns:
        dict: Recommended nutrient values for N, P, K.
    """
     
    # Step 1: Retrieve base nutrient needs from the plant database
    nutrients = plant_database.get(plant, {}).get(growth_stage, {}).copy()
    
    if not nutrients:
        return {"error": "Invalid plant or growth stage"}

    # Step 2: Adjust nutrients based on disease if present
    if disease and disease in disease_adjustments:
        for nutrient, factor in disease_adjustments[disease].items():
            nutrients[nutrient] = nutrients.get(nutrient, 0) * factor
    
    # Step 3: Adjust based on soil data (if available)
    if soil_data:
        if soil_data.get("N", 0) < 10:
            nutrients["N"] *= 1.1  # Increase nitrogen if soil nitrogen is low
        if soil_data.get("P", 0) < 10:
            nutrients["P"] *= 1.1  # Increase phosphorus if soil phosphorus is low
        if soil_data.get("K", 0) < 10:
            nutrients["K"] *= 1.1  # Increase potassium if soil potassium is low

    # Rounding the nutrient recommendations for easy readability
    return {k: round(v, 2) for k, v in nutrients.items()}
    


if __name__ == "__main__":
    plant = sys.argv[1]
    growth_stage = sys.argv[2]
    disease = sys.argv[3] if sys.argv[3] != 'None' else None
    soil_data = {
        "N": float(sys.argv[4]) if sys.argv[4] != 'None' else None,
        "P": float(sys.argv[5]) if sys.argv[5] != 'None' else None,
        "K": float(sys.argv[6]) if sys.argv[6] != 'None' else None
    }
    result = get_fertilizer_recommendation(plant, growth_stage, disease, soil_data)
    print(json.dumps(result))