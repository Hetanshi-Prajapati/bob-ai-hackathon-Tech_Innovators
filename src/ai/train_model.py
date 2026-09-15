import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_FILE = os.path.join(BASE_DIR, "data", "historical_training_data.csv")
MODEL_FILE = os.path.join(os.path.dirname(__file__), "model.pkl")
LABEL_ENCODER_FILE = os.path.join(os.path.dirname(__file__), "label_encoder.pkl")

def train():
    print(f"Loading data from {DATA_FILE}...")
    df = pd.read_csv(DATA_FILE)

    # Encode categorical 'storm_severity'
    le = LabelEncoder()
    df['storm_severity_encoded'] = le.fit_transform(df['storm_severity'])
    
    # Save the label encoder
    joblib.dump(le, LABEL_ENCODER_FILE)

    X = df.drop(columns=['failure_next_7_days', 'storm_severity'])
    y = df['failure_next_7_days']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("\n--- Model Evaluation ---")
    print(f"Accuracy:  {accuracy_score(y_test, y_pred):.2f}")
    print(f"Precision: {precision_score(y_test, y_pred, zero_division=0):.2f}")
    print(f"Recall:    {recall_score(y_test, y_pred, zero_division=0):.2f}")
    print(f"F1-score:  {f1_score(y_test, y_pred, zero_division=0):.2f}")
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print(f"\nSaving model to {MODEL_FILE}...")
    joblib.dump(model, MODEL_FILE)
    print("Done!")

if __name__ == "__main__":
    train()
