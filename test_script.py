import requests

# Loading the inpput file
file_path = "sample.txt" 

load_response = requests.post(
    "http://127.0.0.1:8000/load/",
    json={"file_path": file_path}
)

print("Load Response:")
print("Status Code:", load_response.status_code)
print("Response:", load_response.json())

# If load failed then stop the process
if load_response.status_code != 200:
    exit()

# Asking the question 
question_payload = {
    "question": "What is overfitting?", 
    "top_k": 3
}

ask_response = requests.post(
    "http://127.0.0.1:8000/ask",
    json=question_payload
)

print("\n💬 Ask Response:")
print("Status Code:", ask_response.status_code)
print("Answer:", ask_response.json())
