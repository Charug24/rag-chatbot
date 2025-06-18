import requests

# ========== 1. Load and index the file ==========
file_path = "sample.txt"  # 👈 Change this to your actual file (e.g., sample.pdf, data.csv)

load_response = requests.post(
    "http://127.0.0.1:8000/load/",
    json={"file_path": file_path}
)

print("\n📁 Load Response:")
print("Status Code:", load_response.status_code)
print("Response:", load_response.json())

# Stop here if load failed
if load_response.status_code != 200:
    exit()

# ========== 2. Ask a question ==========
question_payload = {
    "question": "What is overfitting?",  # 👈 Change this to your question
    "top_k": 3
}

ask_response = requests.post(
    "http://127.0.0.1:8000/ask",
    json=question_payload
)

print("\n💬 Ask Response:")
print("Status Code:", ask_response.status_code)
print("Answer:", ask_response.json())
