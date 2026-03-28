# PlasticSense

PlasticSense is a local web app to identify plastic type and advise on reuse/recycle safety.

## Live Demo
- App: https://supportive-peace-production.up.railway.app/
- Health Check: https://supportive-peace-production.up.railway.app/health

## Preview
Add these files in `assets/` to show the live UI on GitHub:
- `assets/hero-ui.png`
- `assets/analyze-demo.gif`

Example markdown to use after you add them:
```md
![PlasticSense UI](assets/hero-ui.png)

![PlasticSense Demo](assets/analyze-demo.gif)
```

## Features
- Analyze by plastic code: PET, HDPE, PVC
- Upload image for ML-based plastic type prediction
- Rule-based decision engine with explanation
- Deployed full-stack app on Railway

## Tech Stack
- Backend: FastAPI
- Frontend: HTML/CSS/JS
- ML: TensorFlow Keras MobileNetV2

## Project Structure
- `backend/`
  - `app.py`: FastAPI entrypoint
  - `decision_engine.py`: rule engine
  - `ml/`: deployed inference model and prediction logic
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

## Recommended Deployment
This project is set up to run as one Python web service on Railway.

- GitHub Pages cannot run FastAPI or TensorFlow because it serves static files only.
- This repository includes `railway.json`, `requirements.txt`, and `runtime.txt` for Railway deployment.
- The FastAPI app serves `index.html`, `styles.css`, and `script.js` directly from the same origin.
- The saved model file `backend/ml/model.h5` is included, so prediction loads a pre-trained model instead of training in production.

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

curl -F "file=@sample.jpg" http://127.0.0.1:8000/analyze-image
```

## Testing
```bash
cd backend
pytest -q
```

## Troubleshooting
- TF logs may show CPU/GPU capability warnings on Railway; these are non-fatal.
- Ensure backend is running for image analysis usage.

