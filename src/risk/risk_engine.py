def calculate_grid_impact(failure_risk, weather_severity, previous_failures, customers_affected):
    """
    Calculates a Grid Impact Score out of 100 based on various risk factors.
    """
    # Weather severity multiplier (Normal: 30, Moderate: 70, Severe: 100)
    weather_score = 100 if weather_severity == 'Severe' else (70 if weather_severity == 'Moderate' else 30)
    
    # Incident score (0 failures = 0, 1 = 50, >1 = 100)
    incident_score = min(100, previous_failures * 50)
    
    # Customer score (assuming 100 max since we capped it to 100, wait, if customers_affected is capped at 100, 
    # we just use it directly. If it's a large number like 22000, we cap the score at 100)
    customer_score = min(100, (customers_affected / 100) * 100) if customers_affected <= 100 else min(100, (customers_affected / 25000) * 100)
    
    # Weighted calculation
    impact_score = (failure_risk * 0.4) + (weather_score * 0.2) + (incident_score * 0.2) + (customer_score * 0.2)
    return int(min(100, impact_score))

def determine_priority(grid_impact):
    if grid_impact >= 90:
        return "P1", "CRITICAL"
    elif grid_impact >= 75:
        return "P2", "HIGH"
    elif grid_impact >= 50:
        return "P3", "MEDIUM"
    else:
        return "P4", "LOW"

def generate_risk_factors(temperature, vibration, oil_quality, weather_severity, previous_failures):
    factors = []
    if temperature > 90:
        factors.append("High temperature")
    if vibration > 7.0:
        factors.append("High vibration")
    if oil_quality < 40:
        factors.append("Poor oil quality")
    if weather_severity == 'Severe':
        factors.append("Severe weather")
    if previous_failures > 0:
        factors.append("Previous failures")
    
    if not factors:
        factors.append("Normal operational parameters")
        
    return factors

def evaluate_asset_risk(prediction, sensor_data, weather_data, incident_data):
    """
    Takes prediction output and context data to produce the final risk profile.
    """
    failure_risk = prediction.get("failure_risk", 0)
    customers = prediction.get("customers_affected", 0)
    
    weather_severity = weather_data.get("storm_severity", "Normal")
    previous_failures = incident_data.get("previous_failures", 0)
    
    grid_impact = calculate_grid_impact(failure_risk, weather_severity, previous_failures, customers)
    priority, risk_level = determine_priority(grid_impact)
    
    risk_factors = generate_risk_factors(
        sensor_data.get("temperature", 0),
        sensor_data.get("vibration", 0),
        sensor_data.get("oil_quality", 100),
        weather_severity,
        previous_failures
    )
    
    # Data Contract Format
    return {
        "equipment_id": prediction.get("equipment_id"),
        "substation_id": prediction.get("substation_id"),
        "equipment_type": "Transformer", # Assuming all are transformers for demo
        "failure_risk": failure_risk,
        "grid_impact": grid_impact,
        "weather_risk": 100 if weather_severity == 'Severe' else (70 if weather_severity == 'Moderate' else 30),
        "priority_score": grid_impact, # For simplicity, tying priority score directly to impact
        "priority": priority,
        "risk_level": risk_level,
        "risk_factors": risk_factors,
        "customers_affected": customers
    }
