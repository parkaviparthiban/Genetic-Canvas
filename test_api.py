import requests

# Check if server is running
try:
    requests.get("http://127.0.0.1:5000")
    print("✅ Server is running")
except requests.exceptions.ConnectionError:
    print("❌ Flask server is not running. Start app.py first.")
    exit()

# Single prediction test
single_url = "http://127.0.0.1:5000/predict"
data = {"sequence": "ATGCGTACGTTAG"}
response = requests.post(single_url, json=data)
print("🔬 Single Prediction:", response.json())

# Batch prediction test
batch_url = "http://127.0.0.1:5000/batch_predict"
files = {"file": open("sample.fasta", "rb")}
response = requests.post(batch_url, files=files)
print("📦 Batch Prediction:", response.json())

# CSV download test
csv_url = "http://127.0.0.1:5000/batch_predict?download=true"
response = requests.post(csv_url, files=files)
with open("predictions.csv", "wb") as f:
    f.write(response.content)
print("📁 CSV saved as predictions.csv")