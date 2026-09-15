import streamlit as st
import pandas as pd
import os
import sys

# Ensure src modules can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from ai.predict import predict
from risk.risk_engine import evaluate_asset_risk
from risk.ibm_integration import generate_granite_recommendation
import ui.dashboard as dashboard

st.set_page_config(page_title="GridGuard AI", layout="wide")

# Paths to data
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

@st.cache_data
def load_data():
    try:
        assets = pd.read_csv(os.path.join(DATA_DIR, "assets.csv"))
        sensors = pd.read_csv(os.path.join(DATA_DIR, "sensor_readings.csv"))
        incidents = pd.read_csv(os.path.join(DATA_DIR, "incident_history.csv"))
        weather = pd.read_csv(os.path.join(DATA_DIR, "weather.csv"))
        return assets, sensors, incidents, weather
    except FileNotFoundError as e:
        st.error(f"Data file not found. Ensure 'data' directory exists and contains the CSVs. ({e})")
        return None, None, None, None

def main():
    dashboard.render_header()
    
    assets, sensors, incidents, weather = load_data()
    if assets is None:
        return
        
    # Process all assets to calculate risks and priorities
    risk_profiles = []
    
    # In a real app this would be optimized, but for a 100-asset demo a loop is fine
    for _, asset_row in assets.iterrows():
        eq_id = asset_row['equipment_id']
        sub_id = asset_row['substation_id']
        
        # Get matching data
        sensor_row = sensors[sensors['equipment_id'] == eq_id].iloc[0].to_dict() if not sensors[sensors['equipment_id'] == eq_id].empty else {}
        incident_row = incidents[incidents['equipment_id'] == eq_id].iloc[0].to_dict() if not incidents[incidents['equipment_id'] == eq_id].empty else {}
        weather_row = weather[weather['substation_id'] == sub_id].iloc[0].to_dict() if not weather[weather['substation_id'] == sub_id].empty else {}
        
        # Prepare sensor data for prediction
        sensor_data = {**sensor_row, 'load_percent': asset_row['load_percent'], 'asset_age': asset_row['asset_age'], 
                       'previous_failures': incident_row.get('previous_failures', 0), 
                       'customers_affected': asset_row['customers_affected'],
                       'equipment_id': eq_id,
                       'substation_id': sub_id,
                       'storm_severity': weather_row.get('storm_severity', 'Normal')}
        
        # 1. Prediction (Member 1)
        try:
            prediction = predict(sensor_data)
        except Exception as e:
            st.error(f"Prediction failed. Ensure model is trained. Error: {e}")
            return
            
        # 2. Risk Engine (Member 2)
        risk_profile = evaluate_asset_risk(prediction, sensor_data, weather_row, incident_row)
        
        # Add full asset details for the UI
        risk_profile.update({
            'temperature': sensor_data.get('temperature'),
            'vibration': sensor_data.get('vibration'),
            'oil_quality': sensor_data.get('oil_quality'),
            'partial_discharge': sensor_data.get('partial_discharge')
        })
        
        risk_profiles.append(risk_profile)
        
    df_risks = pd.DataFrame(risk_profiles)
    
    # Sorting by Priority
    df_risks['priority_rank'] = df_risks['priority'].map({'P1': 1, 'P2': 2, 'P3': 3, 'P4': 4})
    df_risks = df_risks.sort_values(by=['priority_rank', 'failure_risk'], ascending=[True, False])
    
    # 3. Render Summary & Charts (Member 3)
    total_assets = len(df_risks)
    high_risk = len(df_risks[df_risks['risk_level'] == 'HIGH'])
    critical = len(df_risks[df_risks['risk_level'] == 'CRITICAL'])
    
    dashboard.render_summary_cards(total_assets, high_risk, critical)
    dashboard.render_charts(df_risks)
    
    # 4. Render Table
    dashboard.render_priority_table(df_risks)
    
    # 4. Asset Details & IBM AI
    st.markdown("### Inspect Asset")
    selected_asset = st.selectbox("Select Equipment ID to analyze:", df_risks['equipment_id'].tolist())
    
    if selected_asset:
        asset_details = df_risks[df_risks['equipment_id'] == selected_asset].iloc[0].to_dict()
        sub_id = asset_details['substation_id']
        
        weather_row = weather[weather['substation_id'] == sub_id].iloc[0].to_dict() if not weather[weather['substation_id'] == sub_id].empty else {}
        incident_row = incidents[incidents['equipment_id'] == selected_asset].iloc[0].to_dict() if not incidents[incidents['equipment_id'] == selected_asset].empty else {}
        
        # Top Row of Widgets
        w1, w2, w3 = st.columns(3)
        with w1:
            dashboard.render_weather_widget(weather_row)
        with w2:
            dashboard.render_incident_widget(incident_row)
        with w3:
            dashboard.render_sensor_widget(asset_details)
            
        st.markdown("---")
        
        # Risk & AI Section
        r1, r2 = st.columns(2)
        with r1:
            st.markdown(f"#### ⚠️ Risk Profile: {asset_details['risk_level']}")
            st.write(f"- **Failure Risk**: {asset_details['failure_risk']}%")
            st.write(f"- **Grid Impact**: {asset_details['grid_impact']}")
            st.write(f"- **Priority**: {asset_details['priority']}")
            
        with r2:
            # Call IBM Granite (Member 2)
            ibm_recommendation = generate_granite_recommendation(asset_details)
            st.markdown("#### 🤖 IBM Granite Advisor")
            st.info(ibm_recommendation['summary'])
            st.success(ibm_recommendation['crew'])

if __name__ == "__main__":
    main()
