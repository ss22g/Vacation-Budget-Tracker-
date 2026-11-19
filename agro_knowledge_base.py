# agro_knowledge_base.py
# Master Pan-India Agro-Climatic Database & Spatio-Temporal Bio-Filter Engine
# Based on ICAR (Indian Council of Agricultural Research) Regional & Seasonal Classifications.

# 1. Indian Cropping Season Classification (Temporal Layer)
SEASONAL_CROP_CALENDAR = {
    "Auto-Detect / Year-Round (All Seasons)": {
        "description": "Evaluates all ecologically viable regional crops based purely on current soil & climate telemetry.",
        "crops": [
            "rice",
            "wheat",
            "maize",
            "chickpea",
            "pigeonpeas",
            "blackgram",
            "mungbean",
            "mothbeans",
            "lentil",
            "kidneybeans",
            "cotton",
            "jute",
            "sugarcane",
            "banana",
            "mango",
            "grapes",
            "apple",
            "orange",
            "papaya",
            "pomegranate",
            "watermelon",
            "muskmelon",
            "coffee",
            "coconut",
        ],
    },
    "Kharif (Monsoon Sowing: June – October)": {
        "description": "Warm, wet monsoon season crops requiring high humidity and substantial rainfall.",
        "crops": [
            "rice",
            "maize",
            "cotton",
            "jute",
            "pigeonpeas",
            "blackgram",
            "mungbean",
            "mothbeans",
            "sugarcane",
            "banana",
            "papaya",
            "coconut",
            "coffee",
            "mango",
            "pomegranate",
        ],
    },
    "Rabi (Winter Sowing: October – March)": {
        "description": "Cool, dry winter season crops requiring moderate moisture and cool germination temperatures.",
        "crops": [
            "wheat",
            "chickpea",
            "lentil",
            "kidneybeans",
            "maize",
            "grapes",
            "orange",
            "pomegranate",
            "papaya",
            "banana",
            "apple",
        ],
    },
    "Zaid (Summer Sowing: March – June)": {
        "description": "Short-duration summer crops grown between Rabi harvest and Kharif monsoon.",
        "crops": [
            "watermelon",
            "muskmelon",
            "mungbean",
            "blackgram",
            "maize",
            "papaya",
            "banana",
            "mango",
        ],
    },
}

# 2. Pan-India State & District Regional Matrix (Spatial Layer)
PAN_INDIA_REGIONS = {
    "Uttar Pradesh (Eastern / Prayagraj / Varanasi)": {
        "zone": "Middle Gangetic Plain",
        "soil": "Alluvial (Loam / Clay Loam)",
        "def_N": 85,
        "def_P": 42,
        "def_K": 40,
        "def_pH": 7.2,
        "base_temp": 26.5,
        "base_hum": 68.0,
        "base_rain": 195.0,
        "station": "Allahabad",
        "state": "Uttar Pradesh",
        "allowed_crops": [
            "rice",
            "wheat",
            "maize",
            "chickpea",
            "pigeonpeas",
            "lentil",
            "blackgram",
            "mungbean",
            "sugarcane",
            "banana",
            "mango",
            "papaya",
            "watermelon",
            "muskmelon",
        ],
    },
    "Uttar Pradesh (Western / Agra / Meerut)": {
        "zone": "Upper Gangetic Plain",
        "soil": "Alluvial (Sandy Loam)",
        "def_N": 90,
        "def_P": 45,
        "def_K": 42,
        "def_pH": 7.4,
        "base_temp": 25.5,
        "base_hum": 58.0,
        "base_rain": 140.0,
        "station": "Agra",
        "state": "Uttar Pradesh",
        "allowed_crops": [
            "wheat",
            "rice",
            "maize",
            "chickpea",
            "pigeonpeas",
            "lentil",
            "mungbean",
            "sugarcane",
            "watermelon",
            "muskmelon",
            "mango",
        ],
    },
    "Uttar Pradesh (Bundelkhand / Jhansi)": {
        "zone": "Central Plateau & Hills",
        "soil": "Mixed Red & Black (Rakar / Kabar)",
        "def_N": 55,
        "def_P": 25,
        "def_K": 35,
        "def_pH": 6.8,
        "base_temp": 28.5,
        "base_hum": 48.0,
        "base_rain": 125.0,
        "station": "Jhansi",
        "state": "Uttar Pradesh",
        "allowed_crops": [
            "chickpea",
            "pigeonpeas",
            "lentil",
            "blackgram",
            "mothbeans",
            "mungbean",
            "wheat",
            "watermelon",
            "muskmelon",
        ],
    },
    "Punjab & Haryana (Ludhiana / Karnal)": {
        "zone": "Trans-Gangetic Plain",
        "soil": "Fertile Alluvial (Silt Loam)",
        "def_N": 105,
        "def_P": 50,
        "def_K": 48,
        "def_pH": 7.5,
        "base_temp": 24.0,
        "base_hum": 60.0,
        "base_rain": 115.0,
        "station": "Ludhiana",
        "state": "Punjab",
        "allowed_crops": [
            "wheat",
            "rice",
            "maize",
            "cotton",
            "chickpea",
            "mungbean",
            "sugarcane",
            "watermelon",
            "muskmelon",
        ],
    },
    "Rajasthan (Marusthali / Jodhpur / Bikaner)": {
        "zone": "Western Dry Region",
        "soil": "Desert Sandy Soil",
        "def_N": 40,
        "def_P": 20,
        "def_K": 30,
        "def_pH": 8.2,
        "base_temp": 31.0,
        "base_hum": 35.0,
        "base_rain": 65.0,
        "station": "Jodhpur",
        "state": "Rajasthan",
        "allowed_crops": [
            "mothbeans",
            "mungbean",
            "blackgram",
            "chickpea",
            "pomegranate",
            "watermelon",
            "muskmelon",
        ],
    },
    "Madhya Pradesh (Malwa / Indore / Bhopal)": {
        "zone": "Central Plateau & Hills",
        "soil": "Medium Deep Black Cotton Soil",
        "def_N": 70,
        "def_P": 35,
        "def_K": 48,
        "def_pH": 7.8,
        "base_temp": 26.0,
        "base_hum": 60.0,
        "base_rain": 180.0,
        "station": "Bhopal",
        "state": "Madhya Pradesh",
        "allowed_crops": [
            "wheat",
            "chickpea",
            "lentil",
            "maize",
            "pigeonpeas",
            "cotton",
            "blackgram",
            "mungbean",
            "orange",
            "banana",
            "watermelon",
        ],
    },
    "Maharashtra (Vidarbha & Marathwada)": {
        "zone": "Western Plateau & Hills",
        "soil": "Deep Black Regur Soil",
        "def_N": 65,
        "def_P": 30,
        "def_K": 52,
        "def_pH": 8.0,
        "base_temp": 28.0,
        "base_hum": 55.0,
        "base_rain": 160.0,
        "station": "Nagpur",
        "state": "Maharashtra",
        "allowed_crops": [
            "cotton",
            "pigeonpeas",
            "chickpea",
            "blackgram",
            "mungbean",
            "orange",
            "pomegranate",
            "grapes",
            "banana",
            "watermelon",
        ],
    },
    "Gujarat (Saurashtra / Anand)": {
        "zone": "Gujarat Plains & Hills",
        "soil": "Medium Black & Coastal Alluvium",
        "def_N": 75,
        "def_P": 35,
        "def_K": 45,
        "def_pH": 7.9,
        "base_temp": 27.5,
        "base_hum": 65.0,
        "base_rain": 140.0,
        "station": "Ahmedabad",
        "state": "Gujarat",
        "allowed_crops": [
            "cotton",
            "maize",
            "pigeonpeas",
            "chickpea",
            "mungbean",
            "banana",
            "papaya",
            "pomegranate",
            "mango",
            "watermelon",
            "muskmelon",
        ],
    },
    "Bihar (North & South Plains / Patna)": {
        "zone": "Middle Gangetic Plain",
        "soil": "Heavy Alluvial & Terai Soil",
        "def_N": 85,
        "def_P": 40,
        "def_K": 42,
        "def_pH": 7.1,
        "base_temp": 25.8,
        "base_hum": 74.0,
        "base_rain": 220.0,
        "station": "Patna",
        "state": "Bihar",
        "allowed_crops": [
            "rice",
            "wheat",
            "maize",
            "lentil",
            "chickpea",
            "mungbean",
            "banana",
            "mango",
            "jute",
            "sugarcane",
            "watermelon",
        ],
    },
    "West Bengal (Deltaic / Burdwan)": {
        "zone": "Lower Gangetic Plain",
        "soil": "Gangetic Alluvial & Deltaic Clay",
        "def_N": 90,
        "def_P": 45,
        "def_K": 40,
        "def_pH": 6.4,
        "base_temp": 27.0,
        "base_hum": 82.0,
        "base_rain": 280.0,
        "station": "Kolkata",
        "state": "West Bengal",
        "allowed_crops": [
            "rice",
            "jute",
            "banana",
            "mango",
            "papaya",
            "lentil",
            "chickpea",
            "mungbean",
            "watermelon",
        ],
    },
    "Odisha (Coastal & Interior)": {
        "zone": "East Coast Plains & Hills",
        "soil": "Red Laterite & Coastal Deltaic",
        "def_N": 75,
        "def_P": 30,
        "def_K": 38,
        "def_pH": 6.2,
        "base_temp": 27.2,
        "base_hum": 78.0,
        "base_rain": 260.0,
        "station": "Bhubaneswar",
        "state": "Odisha",
        "allowed_crops": [
            "rice",
            "pigeonpeas",
            "blackgram",
            "mungbean",
            "chickpea",
            "coconut",
            "banana",
            "mango",
            "jute",
            "watermelon",
        ],
    },
    "Karnataka (Deccan Plateau / Dharwad)": {
        "zone": "Southern Plateau & Hills",
        "soil": "Red Sandy Loam & Medium Black",
        "def_N": 70,
        "def_P": 35,
        "def_K": 45,
        "def_pH": 6.6,
        "base_temp": 25.0,
        "base_hum": 68.0,
        "base_rain": 170.0,
        "station": "Hubli",
        "state": "Karnataka",
        "allowed_crops": [
            "cotton",
            "maize",
            "pigeonpeas",
            "chickpea",
            "grapes",
            "pomegranate",
            "banana",
            "coconut",
            "watermelon",
        ],
    },
    "Karnataka (Western Ghats / Coorg / Chikmagalur)": {
        "zone": "West Coast Plains & Ghats",
        "soil": "Lateritic Mountain Soil",
        "def_N": 80,
        "def_P": 25,
        "def_K": 35,
        "def_pH": 5.8,
        "base_temp": 22.0,
        "base_hum": 82.0,
        "base_rain": 350.0,
        "station": "Madikeri",
        "state": "Karnataka",
        "allowed_crops": [
            "coffee",
            "coconut",
            "banana",
            "blackgram",
            "papaya",
            "orange",
        ],
    },
    "Kerala (Coastal & Highland)": {
        "zone": "West Coast Plains & Ghats",
        "soil": "Laterite & Coastal Alluvial",
        "def_N": 75,
        "def_P": 25,
        "def_K": 40,
        "def_pH": 5.5,
        "base_temp": 27.5,
        "base_hum": 85.0,
        "base_rain": 380.0,
        "station": "Kochi",
        "state": "Kerala",
        "allowed_crops": [
            "coconut",
            "coffee",
            "banana",
            "rice",
            "papaya",
            "mango",
            "watermelon",
        ],
    },
    "Tamil Nadu (Cauvery Delta / Coimbatore)": {
        "zone": "East Coast Plains & Hills",
        "soil": "Red Sandy Loam & Black Soil",
        "def_N": 80,
        "def_P": 35,
        "def_K": 45,
        "def_pH": 7.2,
        "base_temp": 28.0,
        "base_hum": 72.0,
        "base_rain": 160.0,
        "station": "Tiruchirappalli",
        "state": "Tamil Nadu",
        "allowed_crops": [
            "rice",
            "banana",
            "coconut",
            "cotton",
            "maize",
            "blackgram",
            "mungbean",
            "sugarcane",
            "watermelon",
        ],
    },
    "Andhra Pradesh & Telangana": {
        "zone": "Southern Plateau & East Coast",
        "soil": "Red Sandy & Deep Black (Chalka)",
        "def_N": 75,
        "def_P": 35,
        "def_K": 42,
        "def_pH": 7.4,
        "base_temp": 28.5,
        "base_hum": 65.0,
        "base_rain": 170.0,
        "station": "Vijayawada",
        "state": "Andhra Pradesh",
        "allowed_crops": [
            "rice",
            "cotton",
            "maize",
            "pigeonpeas",
            "chickpea",
            "blackgram",
            "mungbean",
            "banana",
            "mango",
            "papaya",
            "watermelon",
        ],
    },
    "Himachal Pradesh & Kashmir (Temperate Valleys)": {
        "zone": "Western Himalayan Region",
        "soil": "Mountain Brown Forest Soil",
        "def_N": 65,
        "def_P": 35,
        "def_K": 45,
        "def_pH": 6.2,
        "base_temp": 16.0,
        "base_hum": 62.0,
        "base_rain": 180.0,
        "station": "Shimla",
        "state": "Himachal Pradesh",
        "allowed_crops": [
            "apple",
            "kidneybeans",
            "maize",
            "wheat",
            "lentil",
            "pomegranate",
        ],
    },
    "Assam & North-East (Brahmaputra Valley)": {
        "zone": "Eastern Himalayan Region",
        "soil": "Acidic Alluvial & Terai",
        "def_N": 80,
        "def_P": 30,
        "def_K": 35,
        "def_pH": 5.4,
        "base_temp": 24.5,
        "base_hum": 84.0,
        "base_rain": 360.0,
        "station": "Guwahati",
        "state": "Assam",
        "allowed_crops": [
            "rice",
            "jute",
            "banana",
            "papaya",
            "coffee",
            "orange",
            "lentil",
            "maize",
        ],
    },
}


def get_crop_season_badge(crop_name):
    """Returns a clean seasonal badge for any predicted crop."""
    c = crop_name.lower().strip()
    in_kharif = (
        c in SEASONAL_CROP_CALENDAR["Kharif (Monsoon Sowing: June – October)"]["crops"]
    )
    in_rabi = (
        c in SEASONAL_CROP_CALENDAR["Rabi (Winter Sowing: October – March)"]["crops"]
    )
    in_zaid = c in SEASONAL_CROP_CALENDAR["Zaid (Summer Sowing: March – June)"]["crops"]

    seasons = []
    if in_kharif:
        seasons.append("🌧️ Kharif")
    if in_rabi:
        seasons.append("❄️ Rabi")
    if in_zaid:
        seasons.append("☀️ Zaid")

    if len(seasons) >= 2:
        return "🔄 Multi-Season / Year-Round (" + " & ".join(seasons) + ")"
    elif len(seasons) == 1:
        return seasons[0] + " Season Crop"
    return "🌱 Standard Seasonal Crop"


def apply_regional_agronomic_filter(
    crop_probabilities,
    class_labels,
    selected_region_key,
    selected_season_key="Auto-Detect / Year-Round (All Seasons)",
):
    """
    Two-Stage Hybrid Intelligence Bio-Filter:
    Intersects Spatial (ICAR Agro-Climatic Zone) AND Temporal (Kharif / Rabi / Zaid) constraints,
    then re-normalizes probability distribution across viable candidate crops.
    """
    region_info = PAN_INDIA_REGIONS.get(selected_region_key)
    season_info = SEASONAL_CROP_CALENDAR.get(selected_season_key)

    if not region_info:
        return crop_probabilities

    regional_allowed = set(c.lower().strip() for c in region_info["allowed_crops"])

    if season_info:
        seasonal_allowed = set(c.lower().strip() for c in season_info["crops"])
        valid_crops = regional_allowed.intersection(seasonal_allowed)
        if len(valid_crops) < 3:
            valid_crops = regional_allowed
    else:
        valid_crops = regional_allowed

    filtered_probs = crop_probabilities.copy()

    for idx, label in enumerate(class_labels):
        if label.lower().strip() not in valid_crops:
            filtered_probs[idx] = 0.0

    for idx, label in enumerate(class_labels):
        if label.lower().strip() in valid_crops and filtered_probs[idx] == 0.0:
            filtered_probs[idx] = 0.001

    total = sum(filtered_probs)
    if total > 0:
        filtered_probs = [p / total for p in filtered_probs]
    else:
        filtered_probs = crop_probabilities.copy()

    return filtered_probs
