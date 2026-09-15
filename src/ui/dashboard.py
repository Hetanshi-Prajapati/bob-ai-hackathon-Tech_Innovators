import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render_header():
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="font-size: 3.5rem; font-weight: 900; color: #0f62fe; margin-bottom: 0;">GRIDGUARD AI</h1>
            <p style="font-size: 1.2rem; color: #525252; margin-top: -10px; font-weight: bold;">Power Grid Risk Intelligence</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

def render_summary_cards(total_assets, high_risk, critical):
    flip_css = """
    <style>
    .flip-card {
      background-color: transparent;
      width: 100%;
      height: 140px;
      perspective: 1000px;
      margin-bottom: 20px;
    }
    .flip-card-inner {
      position: relative;
      width: 100%;
      height: 100%;
      text-align: center;
      transition: transform 0.6s cubic-bezier(0.4, 0.2, 0.2, 1);
      transform-style: preserve-3d;
      border-radius: 12px;
      box-shadow: 0 4px 8px 0 rgba(0,0,0,0.1);
    }
    .flip-card:hover .flip-card-inner {
      transform: rotateY(180deg);
    }
    .flip-card-front, .flip-card-back {
      position: absolute;
      width: 100%;
      height: 100%;
      -webkit-backface-visibility: hidden;
      backface-visibility: hidden;
      border-radius: 12px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 10px;
    }
    .flip-card-front {
      background: linear-gradient(135deg, #0f62fe, #001d6c);
      color: white;
    }
    .flip-card-back {
      background: linear-gradient(135deg, #f4f4f4, #e0e0e0);
      color: #161616;
      transform: rotateY(180deg);
      border: 2px solid #0f62fe;
    }
    .fc-title { font-size: 1.1rem; opacity: 0.9; margin-bottom: 5px; font-weight: bold;}
    .fc-value { font-size: 2.5rem; font-weight: 900; margin: 0; }
    .fc-back-text { font-size: 1rem; font-weight: 500; }
    </style>
    """
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(flip_css + f"""
<div class="flip-card">
  <div class="flip-card-inner">
    <div class="flip-card-front">
      <div class="fc-title">Total Assets</div>
      <div class="fc-value">{total_assets}</div>
    </div>
    <div class="flip-card-back">
      <div class="fc-back-text">Continuously monitoring {total_assets} grid assets in real-time.</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
<div class="flip-card">
  <div class="flip-card-inner">
    <div class="flip-card-front" style="background: linear-gradient(135deg, #ff832b, #a64200);">
      <div class="fc-title">High Risk Warnings</div>
      <div class="fc-value">{high_risk}</div>
    </div>
    <div class="flip-card-back" style="border-color: #ff832b;">
      <div class="fc-back-text">{high_risk} assets showing elevated failure probabilities.</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
<div class="flip-card">
  <div class="flip-card-inner">
    <div class="flip-card-front" style="background: linear-gradient(135deg, #da1e28, #750e13);">
      <div class="fc-title">Critical Alerts</div>
      <div class="fc-value">{critical}</div>
    </div>
    <div class="flip-card-back" style="border-color: #da1e28;">
      <div class="fc-back-text">Immediate AI dispatch required for {critical} critical failures.</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
        
    st.markdown("---")

def render_charts(df):
    st.markdown("### Grid Health Analytics")
    col1, col2 = st.columns(2)
    
    with col1:
        priority_counts = df['priority'].value_counts().reset_index()
        priority_counts.columns = ['Priority', 'Count']
        fig1 = px.pie(priority_counts, values='Count', names='Priority', 
                     hole=0.6, title="Asset Priority Breakdown",
                     color='Priority',
                     color_discrete_map={'P1':'#da1e28', 'P2':'#ff832b', 'P3':'#f1c21b', 'P4':'#24a148'})
        
        fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=40, b=0, l=0, r=0))
        st.plotly_chart(fig1, use_container_width=True)
        
    with col2:
        fig2 = px.scatter(df, x='temperature', y='vibration', color='risk_level',
                          size='failure_risk', hover_data=['equipment_id'],
                          title="Temperature vs Vibration vs Risk",
                          color_discrete_map={'CRITICAL':'#da1e28', 'HIGH':'#ff832b', 'MEDIUM':'#f1c21b', 'LOW':'#24a148'})
        
        fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig2, use_container_width=True)
        
    st.markdown("---")

def render_priority_table(df):
    st.markdown("### Priority Asset Roster")
    display_df = df[['equipment_id', 'substation_id', 'failure_risk', 'risk_level', 'priority']]
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# -------------------------------------------------------------
# Custom Widgets
# -------------------------------------------------------------

def render_weather_widget(weather):
    severity = weather.get('storm_severity', 'Normal')
    temp = weather.get('temperature', 0)
    precip = weather.get('precipitation', 0)
    
    if severity == 'Normal':
        bg = "linear-gradient(to bottom, #87CEEB, #e0f6ff)"
        animation_html = "<div style='font-size: 50px; text-align: center; margin-top: 10px;'>☀️</div>"
    elif severity == 'Warning':
        bg = "linear-gradient(to bottom, #bdc3c7, #2c3e50)"
        animation_html = "<div style='font-size: 50px; text-align: center; margin-top: 10px; animation: pulse 2s infinite;'>☁️🌧️</div>"
    else: # Severe
        bg = "linear-gradient(to bottom, #373b44, #4286f4)"
        animation_html = "<div style='font-size: 50px; text-align: center; margin-top: 10px; animation: flash 1.5s infinite;'>⛈️⚡</div><style>@keyframes flash { 0% {opacity: 1;} 50% {opacity: 0.3;} 100% {opacity: 1;} }</style>"

    html_content = f"""
<style>
.widget-hover {{
    transition: transform 0.3s cubic-bezier(0.4, 0.2, 0.2, 1), box-shadow 0.3s ease;
}}
.widget-hover:hover {{
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 10px 20px rgba(0,0,0,0.2) !important;
}}
</style>
<div class="widget-hover" style="background: {bg}; border-radius: 10px; padding: 20px; color: white; min-height: 200px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); display: flex; flex-direction: column; justify-content: center; align-items: center;">
    <h4 style="margin: 0; color: white; text-align: center;">Live Weather Tracker</h4>
    {animation_html}
    <div style="text-align: center; margin-top: 15px; font-size: 1.1rem; font-weight: bold;">
        {severity.upper()} | {temp}°C | {precip}mm Rain
    </div>
</div>
"""
    st.markdown(html_content, unsafe_allow_html=True)

def render_sensor_widget(sensor):
    temp = sensor.get('temperature', 0)
    vib = sensor.get('vibration', 0)
    
    # Plotly Gauge Chart for Temperature
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = temp,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Core Temp (°C)"},
        gauge = {
            'axis': {'range': [0, 120]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 60], 'color': "lightgreen"},
                {'range': [60, 85], 'color': "gold"},
                {'range': [85, 120], 'color': "salmon"}
            ]
        }
    ))
    fig.update_layout(height=180, margin=dict(l=20, r=20, t=30, b=10), paper_bgcolor="rgba(0,0,0,0)")
    
    st.plotly_chart(fig, use_container_width=True)
    st.caption(f"Vibration Level: **{vib:.2f} G** | Oil Quality: **{sensor.get('oil_quality')}**")

def render_incident_widget(incident):
    failures = incident.get('previous_failures', 0)
    days_since = incident.get('days_since_last_maintenance', 0)
    
    bg_color = "#da1e28" if failures > 2 else "#ff832b" if failures > 0 else "#24a148"
    status_text = "CRITICAL HISTORY" if failures > 2 else "WARNING" if failures > 0 else "HEALTHY"
    
    st.markdown(f"""
    <div class="widget-hover" style="background-color: {bg_color}; border-radius: 10px; padding: 20px; color: white; min-height: 200px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); display: flex; flex-direction: column; justify-content: center; align-items: center;">
        <h4 style="margin: 0; color: white;">Incident Log</h4>
        <div style="font-size: 1.5rem; font-weight: 900; margin: 10px 0;">{status_text}</div>
        <div style="font-size: 1rem;">Past Failures: <b>{failures}</b></div>
        <div style="font-size: 1rem;">Days since maint: <b>{days_since}</b></div>
    </div>
    """, unsafe_allow_html=True)
