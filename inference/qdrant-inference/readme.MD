

python3 -m venv qdrant-inference-env

source qdrant-inference-env/bin/activate

pip install -r requirements.txt


uvicorn main:app --host 0.0.0.0 --port 8080