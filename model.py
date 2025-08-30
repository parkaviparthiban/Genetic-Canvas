import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def train_model(X, y):
    """
    Trains a RandomForest model and saves it to disk.
    """
    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"✅ Model trained with accuracy: {acc:.2f}")
        with open("output/dna_model.pkl", "wb") as f:
            pickle.dump(model, f)
        print("💾 Model saved to output/dna_model.pkl")
    except Exception as e:
        print(f"❌ Model training failed: {e}")