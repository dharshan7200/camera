frontend:
  python -m http.server 5500

backend:
   pip install -r requirements.txt
   python -m uvicorn main:app --reload
