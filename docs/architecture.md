# Architecture

```mermaid
flowchart TD
    subgraph Data Sources
        S[Sensor Data]
        W[Weather Data]
        I[Incident History]
        A[Asset Data]
    end

    subgraph Prediction Engine (Member 1)
        RF[Random Forest Classifier]
        FP[Failure Probability %]
    end

    subgraph Decision Engine (Member 2)
        RE[Risk Engine]
        GIS[Grid Impact Score]
        PR[Priority Ranking]
        IBM[IBM Granite / Watsonx.ai]
    end

    subgraph Visualization (Member 3)
        UI[Streamlit Dashboard]
    end

    S --> RF
    I --> RF
    W --> RF
    A --> RF
    
    RF --> FP
    
    FP --> RE
    W --> RE
    I --> RE
    A --> RE
    
    RE --> GIS
    GIS --> PR
    
    PR --> IBM
    IBM --> UI
    
    PR --> UI
```

### Member Contributions
- **Member 1 (Data & ML)**: Historical data generation, ML training, Random Forest inference.
- **Member 2 (Risk & GenAI)**: Grid Impact calculus, Priority assignments, IBM Watsonx integration for generative plans.
- **Member 3 (UI)**: Streamlit visual analytics, tables, and asset inspection pane.
- **Member 4 (Integration)**: `app.py` orchestration, API mock fallbacks, application flow.
