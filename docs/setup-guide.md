# Setup Guide

This guide allows you to run the GridGuard AI application from scratch locally.

## Prerequisites
- Python 3.8+
- Git

## Installation

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd bob-ai-hackathon-Tech_Innovators
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Train the ML Model**
   Generate the `model.pkl` used for predicting equipment failure:
   ```bash
   python src/ai/train_model.py
   ```

4. **Environment Variables (Optional)**
   The app provides a robust mock for IBM WatsonX/Granite integration so it functions flawlessly out-of-the-box. If you wish to use live IBM WatsonX credentials:
   - Create a `.env` file at the root.
   - Add `IBM_CLOUD_API_KEY=your_key_here`
   - Add `WATSONX_PROJECT_ID=your_id_here`

5. **Start the Application**
   ```bash
   streamlit run app.py
   ```

6. **Usage**
   - Open your browser to `http://localhost:8501`.
   - The dashboard will display all predicted risks and priorities.
   - Select an asset from the dropdown (e.g., `TX-104`) to view the deep-dive analysis and AI recommendations.
