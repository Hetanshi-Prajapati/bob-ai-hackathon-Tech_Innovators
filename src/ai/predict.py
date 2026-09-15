import json
import joblib
import os
import sys
import pandas as pd

MODEL_FILE = os.path.join(os.path.dirname(__file__), "model.pkl")
LABEL_ENCODER_FILE = os.path.join(os.path.dirname(__file__), "label_encoder.pkl")

_MODEL = None
_LE = None

def load_model():
    global _MODEL, _LE
    if _MODEL is not None and _LE is not None:
        return _MODEL, _LE
        
    if not os.path.exists(MODEL_FILE) or not os.path.exists(LABEL_ENCODER_FILE):
        print(f"Error: Model or encoder not found. Run train_model.py first.")
        sys.exit(1)
        
    _MODEL = joblib.load(MODEL_FILE)
    _LE = joblib.load(LABEL_ENCODER_FILE)
    return _MODEL, _LE

def predict(sensor_data):
    """
    Expects sensor_data dict matching historical training features:
    temperature, vibration, oil_quality, partial_discharge, load_percent, asset_age, previous_failures, storm_severity
    """
    model, le = load_model()
    
    # Handle missing or unseen categories gracefully
    severity = sensor_data.get("storm_severity", "Normal")
    if severity not in le.classes_:
        severity_encoded = 0 # default fallback
    else:
        severity_encoded = le.transform([severity])[0]
        
    sensor_data['storm_severity_encoded'] = severity_encoded
    
    features = ['temperature', 'vibration', 'oil_quality', 'partial_discharge', 
                'load_percent', 'asset_age', 'previous_failures', 'storm_severity_encoded']
    
    X = pd.DataFrame([{feature: sensor_data.get(feature, 0) for feature in features}])
    
    prob = model.predict_proba(X)[0][1]
    
    result = {
        "equipment_id": sensor_data.get("equipment_id", "UNKNOWN"),
        "substation_id": sensor_data.get("substation_id", "UNKNOWN"),
        "failure_risk": int(prob * 100),
        "customers_affected": sensor_data.get("customers_affected", 0)
    }
    
    return result

if __name__ == "__main__":
    demo_scenario = {
        "equipment_id": "TX-104",
        "substation_id": "SUB-C",
        "temperature": 101,
        "vibration": 9.1,
        "oil_quality": 29,
        "partial_discharge": 93,
        "load_percent": 95,
        "asset_age": 19,
        "previous_failures": 4,
        "customers_affected": 22000,
        "storm_severity": "Severe"
    }
    
    prediction = predict(demo_scenario)
    print(json.dumps(prediction, indent=2))
