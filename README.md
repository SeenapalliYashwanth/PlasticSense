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
- Root directory: single-page web UI (`index.html`, `script.js`, `styles.css`)

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
Open `index.html` directly or use VS Code Live Server.

## GitHub Pages
- GitHub Pages can host the static frontend from the repository root.
- The dropdown analysis works directly in the browser without the backend.
- The image upload feature still needs the FastAPI backend on a public URL.
- After deploying the backend, set `CONFIGURED_API_URL` in `script.js` to that backend URL.

## Recommended Deployment
For full frontend + backend + ML support, deploy the whole app as one Python web service instead of relying only on GitHub Pages.

- GitHub Pages cannot run FastAPI or TensorFlow because it serves static files only.
- This repository now includes `render.yaml` and `railway.json` so you can deploy the full app on Render or Railway.
- The FastAPI app serves `index.html`, `styles.css`, and `script.js` directly from the same origin.
- The saved model file `backend/ml/model.h5` is included, so prediction can load the model instead of retraining on first request.

### Render Steps
1. Push this code to GitHub.
2. Sign in to Render and create a new Blueprint or Web Service from this repository.
3. Render will use:
   - Build command: `pip install -r backend/requirements.txt`
   - Start command: `uvicorn backend.app:app --host 0.0.0.0 --port $PORT`
4. Open the deployed URL and use the app there. The frontend and backend will be connected automatically.

### Railway Steps
1. Push this code to GitHub.
2. Create a new Railway project from the repository.
3. Railway can use the root `requirements.txt` and `railway.json` in this repo.
4. Open the deployed URL and use the app there. The frontend and backend will be connected automatically.

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
- Ensure backend is running for image analysis usage.

