# RAG-Based HR Policy Chatbot (FastAPI + Docker)


A fully containerized Question Answering system that uses **Retrieval-Augmented Generation** to extract information from documents in PDF, TXT, or CSV format.

---

## 🚀 Features

- Accepts PDF, TXT, and CSV documents
- Chunks, embeds, and stores in FAISS vector DB
- RESTful API (via FastAPI)
- Groq API is used to generate answers from llama3-70b-8192 model
- Dockerised

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourname/rag-chatbot.git
cd rag-bot
```
## Build Docker Image

```bash
docker build -t rag-chatbot:1 .
```
## Run the container

```bash
docker run -p 8000:8000 rag-chatbot:1

```

## Testing instructions

A sample test script test_script.py is provided. It uploads a file and asks a question automatically.

``` bash
python3 test_script.py

```

## Running the code

Install the requirements mentioned in the `requirements.txt` 

Place your input file in the root folder and mention the path of the file in `test_script.py`.

To run the code, run the docker image in one terminal and in another terminal run the `test_script.py`

##  Example Input Documents

| File Name          | Type | 
|--------------------|------|
| `sample.txt`       | TXT  | 


## Example Questions & Expected Output

### API Payload:

```json
{
  "question": "What is overfitting",
}
```

### Sample Response

```json
{
  "answer": "According to the context, overfitting occurs when a model performs well on training data but poorly on unseen data."
}
```



