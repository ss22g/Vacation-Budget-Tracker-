"""
soil_methodology_engine.py
Enterprise Soil Chemical Diagnostics & Multi-Method Intake Engine
Calculates confidence degradation, nutrient fixation alerts, and regional pedology.
"""

# Master Pedological Classifications with Micro-Nutrient & Texture Metrics
SOIL_ARCHETYPES = {
    "1. Indo-Gangetic Alluvial Soil (Loam / Silt Loam)": {
        "N": 85, "P": 45, "K": 40, "pH": 7.2,
        "texture": "Medium Loam",
        "organic_carbon": "0.55% (Medium)",
        "permeability": "High",
        "limiting_note": "Prone to Nitrogen volatilization and leaching under heavy irrigation."
    },
    "2. Deep Black Cotton Soil (Deccan Regur / Heavy Clay)": {
        "N": 65, "P": 28, "K": 52, "pH": 8.1,
        "texture": "Heavy Clay (Montmorillonite)",
        "organic_carbon": "0.45% (Low-Medium)",
        "permeability": "Low (High water retention, crack formation)",
        "limiting_note": "High swelling and shrinkage; susceptible to waterlogging in monsoon."
    },
    "3. Red Sandy & Loamy Soil (Southern / Eastern Plateau)": {
        "N": 55, "P": 22, "K": 35, "pH": 6.4,
        "texture": "Coarse Sandy Loam",
        "organic_carbon": "0.35% (Low)",
        "permeability": "Very High",
        "limiting_note": "Low cation exchange capacity (CEC); rapid nutrient leaching."
    },
    "4. Lateritic Mountain & Ghat Soil (Highland Leached)": {
        "N": 75, "P": 18, "K": 32, "pH": 5.4,
        "texture": "Porous Cellular Clay",
        "organic_carbon": "0.85% (High in forests)",
        "permeability": "Rapid Drainage",
        "limiting_note": "High acidity causes strong Phosphorus fixation (insoluble iron/aluminum phosphates)."
    },
    "5. Desert & Semi-Arid Sandy Soil (Thar / Western Region)": {
        "N": 38, "P": 18, "K": 28, "pH": 8.3,
        "texture": "Loose Dune Sand",
        "organic_carbon": "0.15% (Very Low)",
        "permeability": "Excessive",
        "limiting_note": "Poor moisture-holding capacity and high salinity / alkalinity potential."
    },
    "6. Deltaic Alluvium & Coastal Saline Soil": {
        "N": 90, "P": 38, "K": 45, "pH": 6.8,
        "texture": "Silty Clay Clayey Delta",
        "organic_carbon": "0.75% (High)",
        "permeability": "Moderate to Slow",
        "limiting_note": "Requires periodic monitoring for coastal salt ingress."
    }
}

# Empirical Symptom-to-Nutrient Mapping
VISUAL_SYMPTOM_DIAGNOSTICS = {
    "1. General Chlorosis: Lower leaves turn pale yellow starting from tip down midrib": {
        "N": 30, "P": 45, "K": 45, "pH": 6.8,
        "diagnosis": "Severe Nitrogen (N) Starvation",
        "recommendation": "Apply fast-acting Nitrogen (Neem-coated urea or split fertigation) before panicle/flowering stage."
    },
    "2. Anthocyanin Pigmentation: Dark purple/bronze foliage with stunted root development": {
        "N": 85, "P": 12, "K": 45, "pH": 6.8,
        "diagnosis": "Severe Phosphorus (P) Deficiency",
        "recommendation": "Supplement with basal Di-Ammonium Phosphate (DAP) or Single Super Phosphate (SSP) directly near root zones."
    },
    "3. Marginal Necrosis: Burnt leaf margins, curling edges, and weak stem lodging": {
        "N": 85, "P": 42, "K": 18, "pH": 6.8,
        "diagnosis": "Acute Potassium (K) Depletion",
        "recommendation": "Apply Muriate of Potash (MOP) to restore plant vascular turgor and pest immunity."
    },
    "4. Interveinal Chlorosis on Acidic Soil: Veins stay green while leaf tissue yellows": {
        "N": 70, "P": 25, "K": 35, "pH": 5.2,
        "diagnosis": "Soil Acidity Induced Nutrient Lockup (Mg/P lock)",
        "recommendation": "Broadcast agricultural lime (CaCO3) or dolomite to raise soil pH closer to neutral 6.5."
    },
    "5. Healthy Uniform Dark Green Canopy: Vigorous vegetative growth with normal tillering": {
        "N": 92, "P": 44, "K": 44, "pH": 6.6,
        "diagnosis": "Balanced Macro-Nutrient Profile",
        "recommendation": "Maintain standard maintenance dosage based on planned crop extraction targets."
    }
}

def analyze_soil_health(N, P, K, ph):
    """
    Evaluates nutrient proportions and flags chemical lockup risks.
    """
    alerts = []

    # pH analysis
    if ph < 5.5:
        alerts.append("🔴 **High Soil Acidity (pH < 5.5):** High risk of Phosphorus fixation by active Aluminum/Iron. Micronutrient toxicities possible.")
    elif ph > 8.2:
        alerts.append("🟡 **Soil Alkalinity / Salinity (pH > 8.2):** High free Calcium limits availability of Phosphorus, Zinc, and Iron.")
    else:
        alerts.append("🟢 **Optimum Soil Reaction (pH 6.0 - 7.5):** Maximum availability of essential N-P-K macro-nutrients.")

    # Nitrogen to Potassium ratio analysis
    if K > 0:
        nk_ratio = N / K
        if nk_ratio > 3.0:
            alerts.append("⚠️ **High N:K Ratio:** Excess vegetative growth may cause stem lodging and increase vulnerability to fungal blast and pest attacks.")

    return alerts