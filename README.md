# GridGuard AI

**Power-grid transformers/substations can fail and cause outages.** We want to detect risky equipment before it fails by combining equipment health, weather, and historical incidents.

GridGuard AI is an end-to-end intelligence platform that helps grid operators predict equipment failures, prioritize maintenance based on grid impact, and generate actionable AI-driven crew recommendations.

## The Solution: Predict → Prioritize → Explain → Act

1. **Predict**: Machine Learning (Random Forest) predicts failure probability based on sensor health, load, and age.
2. **Prioritize**: Risk Engine combines failure probability with weather severity and incident history to calculate Grid Impact.
3. **Explain & Act**: IBM Granite generates maintenance instructions and recommends crew pre-positioning.

## Architecture

![Architecture](docs/architecture.md)

- **Frontend**: Streamlit Dashboard
- **Backend/Integration**: Python
- **AI/ML**: Scikit-Learn (Random Forest)
- **Generative AI**: IBM Watsonx / Granite

## How to Run

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the ML pipeline to train the model:
   ```bash
   python src/ai/train_model.py
   ```
4. Start the application:
   ```bash
   streamlit run app.py
   ```

## Key Features
- **Risk Map & Summary**: At-a-glance view of the grid's health.
- **Priority Table**: Ranked list of critical assets requiring attention.
- **AI Maintenance Advisor**: IBM Granite-powered maintenance plans.

## Demo Scenario
To test the core killer scenario, select asset `TX-104` in the dashboard to see an end-to-end critical risk evaluation and crew pre-positioning recommendation.

## Future Scope
- Live IoT sensor streaming integration.
- Real-time weather API integration (e.g., The Weather Company).
- Automated work order creation in Maximo.
