import os
import threading

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

# import from the package context
from backend.decision_engine import analyze_plastic
from backend.ml.predict import predict_plastic_type, warmup_model

app = FastAPI(title="PlasticSense API")
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# enable CORS for local development and for the GitHub Pages frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:3000",
        "http://localhost:3000",
        "http://127.0.0.1:8000",
        "https://seenapalliyashwanth.github.io",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.on_event("startup")
def preload_model():
    # Warm the ML model in the background so the first image request is faster.
    threading.Thread(target=warmup_model, daemon=True).start()

@app.get("/analyze")
def analyze(plastic_type: str):
    return analyze_plastic(plastic_type.upper())


@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    try:
        plastic_type = predict_plastic_type(file.file)
    except Exception as e:
        # Keep user-friendly response but include detail in logs
        detail = str(e)
        print(f"ML model inference failed: {detail}")

        # Use 422 to indicate client-provided image cannot be classified reliably
        return JSONResponse(
            status_code=422,
            content={
                "error": "ML inference failed",
                "detail": detail,
                "recommendation": "Please try a clearer picture or choose a different angle, or use the dropdown selection instead."
            },
        )

    # Ensure we don't propagate model errors into circulatory logic
    if not plastic_type or not isinstance(plastic_type, str):
        print(f"ML returned invalid type: {plastic_type!r}")
        return JSONResponse(
            status_code=422,
            content={
                "error": "ML inference returned invalid type",
                "detail": f"Unexpected model output: {plastic_type!r}",
            },
        )

    result = analyze_plastic(plastic_type)
    result["detected_by"] = "ML Image Analysis"
    return result


# Keep API routes above this mount so one deployment can serve the
# frontend and backend from the same origin.
app.mount("/", StaticFiles(directory=PROJECT_ROOT, html=True), name="frontend")
