# Solution Overview

GridGuard AI is a comprehensive predictive maintenance solution built specifically for power grid infrastructure.

## Data Integration
The system ingests data from four distinct streams:
1. **Sensor Data**: IoT measurements like temperature, vibration, oil quality, and partial discharge.
2. **Weather Data**: Localized forecasts including storm severity and wind speed.
3. **Incident History**: Past failure records and time since last incident.
4. **Asset Metadata**: Age, load capacity, and customer exposure.

## Predictive ML Engine
A Random Forest Classifier trained on historical synthetic data evaluates the incoming data streams to predict a precise Failure Risk percentage for the next 7 days.

## Risk & Priority Engine
Instead of just flagging high-risk equipment, the Risk Engine combines the Failure Risk with Weather Severity, Customer Exposure, and Incident History to calculate a 0-100 `Grid Impact Score`. This dictates a Priority Level (P1 to P4).

## Generative AI Action
Using IBM Granite / Watsonx.ai, the structured risk profile is translated into an actionable maintenance and dispatch plan, helping operators know exactly *what* to do, *why* it's urgent, and *who* to send.
