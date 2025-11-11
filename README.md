# 🧠 Plagiarism Checker API & Web App  

A complete plagiarism detection system built with **Flask**, **Streamlit**, and **Kong API Gateway** — demonstrating **AI-powered text similarity**, **rate limiting**, and **payload size control**.  

---

## 🚀 Project Overview  

This project allows users to upload two text files — an original and a submission — and checks for textual similarity using **cosine similarity** and an ML-based probability model.  

It includes:
- A **Flask REST API** for file upload and similarity computation.  
- A **Streamlit Web UI** for interactive usage.  
- A **Kong API Gateway** setup for request control (rate-limiting, payload-size limiting).  
- **Token Bucket** and **Leaky Bucket** algorithms for rate-limiting demonstrations.  

---

## 🧩 Features  

| Component | Description |
|------------|-------------|
| 🧮 **Flask API** | Handles `/check` endpoint for text comparison. |
| 🌐 **Streamlit UI** | Simple frontend to upload and visualize results. |
| 🛡️ **Kong Gateway** | Rate limit: 5 requests/min; Payload limit: 1 KB. |
| ⚙️ **ML Model** | Logistic Regression using cosine similarity score. |
| 📈 **Algorithms** | Token Bucket & Leaky Bucket rate-limiting simulation scripts. |

---

## 🏗️ Project Structure  

plagarism_check/
├── flask_api/
│ ├── app.py # Flask API server
│ ├── model.py # ML model creation
│ ├── utils.py # Similarity & highlight functions
│ └── plagiarism_model.pkl # Saved ML model
│
├── streamlit_app/
│ └── app.py # Streamlit UI app
│
├── sample_data/
│ ├── original.txt
│ └── submission.txt
│
├── kong.yml # Kong declarative config
├── temp.sh # Script to test rate-limit behavior
├── token_bucket.py # Token bucket demo
├── leaky_bucket.py # Leaky bucket demo
└── README.md

## ⚙️ Setup Instructions  

### 🧰 1. Clone the Repo

git clone https://github.com/<your-username>/plagiarism-checker.git
cd plagiarism-checker
🐍 2. Setup Python Environment

python -m venv .venv
source .venv/bin/activate     # (on Windows: .venv\Scripts\activate)
pip install -r requirements.txt
If you don’t have requirements.txt, run:


pip install flask streamlit joblib scikit-learn numpy requests
🧠 3. Train the Model (once)

python flask_api/model.py
This creates the trained model file:
flask_api/plagiarism_model.pkl

⚡ 4. Run Flask API

python flask_api/app.py
Server starts at:


http://127.0.0.1:5000
Test it:


curl -F "original=@sample_data/original.txt" \
     -F "submission=@sample_data/submission.txt" \
     http://127.0.0.1:5000/check
🖥️ 5. Run Streamlit App
In another terminal:


streamlit run streamlit_app/app.py --server.address 127.0.0.1 --server.port 8501
Open in browser:
👉 http://127.0.0.1:8501

🐳 6. Setup Kong Gateway (Docker)
Create network:

docker network create kong-net
Run Kong in DB-less mode:

docker run -d --name kong-dbless --network=kong-net \
  -v "$(pwd)/kong.yml:/usr/local/kong/declarative/kong.yml:ro" \
  -e KONG_DATABASE=off \
  -e KONG_DECLARATIVE_CONFIG=/usr/local/kong/declarative/kong.yml \
  -p 8000:8000 -p 8443:8443 -p 8001:8001 \
  kong:3.0.0
Kong admin: http://localhost:8001
Kong proxy: http://localhost:8000

🔬 Test Kong Rate Limiting
Run multiple requests via:


bash temp.sh
Expected output:


=== RATE-LIMIT LOOP (8 attempts) ===
attempt 1 -> HTTP 200
attempt 2 -> HTTP 200
...
attempt 6 -> HTTP 429
attempt 7 -> HTTP 429
attempt 8 -> HTTP 429
🧮 Token & Leaky Bucket Demos
Token Bucket

python token_bucket.py
Expected output:


TokenBucket: capacity=5, refill=1/sec - try 12 requests (0.6s apart)
01: allowed=True, tokens_left=4.00
...
12: allowed=False, tokens_left=0.61
Leaky Bucket

python leaky_bucket.py
Expected output:

LeakyBucket: capacity=3, leak=0.5/sec - try 10 requests (0.6s apart)
01: enqueued (queue=1)

10: dropped (queue=3)
