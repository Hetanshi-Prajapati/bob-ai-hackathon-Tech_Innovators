import os
import requests
import json

def generate_granite_recommendation(risk_profile):
    """
    Sends the risk profile to Local Llama 3 (via Ollama) for recommendations.
    Provides a robust mock fallback if Ollama is not running locally.
    """
    # Create the prompt for Llama 3
    prompt = f"""
    You are an expert AI maintenance advisor for a power grid. 
    Analyze this asset and provide a short summary, maintenance actions, and crew dispatch plan.
    
    Asset Details:
    Equipment: {risk_profile.get('equipment_id')}
    Priority: {risk_profile.get('priority')}
    Failure Risk: {risk_profile.get('failure_risk')}%
    Risk Factors: {risk_profile.get('risk_factors')}
    
    You MUST respond with ONLY a valid JSON object in this exact format, with no other text:
    {{
        "summary": "1 sentence summarizing the situation",
        "maintenance": ["action 1", "action 2"],
        "crew": "1 sentence dispatch plan"
    }}
    """
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "stream": False,
                "format": "json"
            },
            timeout=10
        )
        if response.status_code == 200:
            result = response.json()
            llm_text = result.get("response", "{}")
            parsed_json = json.loads(llm_text)
            
            # Ensure the structure matches the UI expectations
            return {
                "summary": parsed_json.get("summary", "Analysis complete."),
                "maintenance": parsed_json.get("maintenance", ["Monitor asset."]),
                "crew": parsed_json.get("crew", "No immediate crew action."),
                "priority_label": risk_profile.get("priority", "Unknown")
            }
    except Exception as e:
        # If Ollama is not running, gracefully fallback to the mock logic
        print(f"Ollama connection failed ({e}). Falling back to mock data.")
        
    return _generate_mock_recommendation(risk_profile)

def _generate_mock_recommendation(risk_profile):
    equipment_id = risk_profile.get("equipment_id", "Unknown")
    priority = risk_profile.get("priority", "P4")
    risk_factors = risk_profile.get("risk_factors", [])
    
    if priority == "P1":
        factors_str = ", ".join([f.lower() for f in risk_factors])
        summary = f"{equipment_id} has critical failure risk due to {factors_str}."
        maintenance = [
            "Inspect within 24 hours",
            "Check cooling system",
            "Perform oil-quality inspection"
        ]
        crew = "Pre-position Crew 2 near the substation."
    elif priority == "P2":
        summary = f"{equipment_id} shows high risk indicators requiring scheduled attention."
        maintenance = [
            "Schedule inspection within 7 days",
            "Monitor vibration levels"
        ]
        crew = "Alert maintenance team for upcoming dispatch."
    elif priority == "P3":
        summary = f"{equipment_id} has medium risk factors. Continue monitoring."
        maintenance = [
            "Review sensor data in 30 days"
        ]
        crew = "No immediate crew action required."
    else:
        summary = f"{equipment_id} is operating normally with low risk."
        maintenance = [
            "Routine annual maintenance"
        ]
        crew = "No crew action required."
        
    return {
        "summary": summary,
        "maintenance": maintenance,
        "crew": crew,
        "priority_label": f"{priority} — {'Immediate attention' if priority == 'P1' else ('High priority' if priority == 'P2' else 'Standard')}"
    }
