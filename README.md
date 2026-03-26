# PlasticSense

PlasticSense is a local web app to identify plastic type and advise on reuse/recycle safety.

## Features
- Analyze by plastic code: PET, HDPE, PVC
- Upload image for ML-based plastic type prediction
- Rule-based decision engine with explanation
- CORS support for local frontend calls

## Tech Stack
- Backend: FastAPI
- Frontend: HTML/CSS/JS
- ML: TensorFlow Keras MobileNetV2

## Project Structure
- `backend/`
  - `app.py`: FastAPI entrypoint
  - `decision_engine.py`: rule engine
  - `ml/`: model training/prediction and dataset
  - `plastic_rules.json`: safety definitions
- `frontend/`: single-page web UI (`index.html`, `script.js`, `styles.css`)

## Setup
1. Create virtualenv (recommended):
   ```bash
   python -m venv venv
   venv\\Scripts\\activate  # Windows
   source venv/bin/activate   # macOS/Linux
   ```
2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

## Run Backend
```bash
cd c:\\Users\\PC\\Desktop\\PlasticSense
C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python310\\python.exe -m uvicorn backend.app:app --reload
```

## Run Frontend
Open `frontend/index.html` directly or use VS Code Live Server.

## API Endpoints
- `GET /analyze?plastic_type=PET|HDPE|PVC`
- `POST /analyze-image` (multipart `file`)

### Example
```bash
curl "http://127.0.0.1:8000/analyze?plastic_type=PET"

curl -F "file=@backend/ml/dataset/PET/000001.jpg" http://127.0.0.1:8000/analyze-image
```

## Testing
```bash
cd backend
pytest -q
```

## Troubleshooting
- If ML fails with InputLayer / batch_shape errors: model is rebuilt from scratch and dataset training is triggered.
- TF logs may show a deprecation warning from `tf.losses.sparse_softmax_cross_entropy`; this is non-fatal.
- Ensure backend is running before frontend usage.

