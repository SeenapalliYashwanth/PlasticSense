from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# import from the package context
from backend.decision_engine import analyze_plastic
from backend.ml.predict import predict_plastic_type
app = FastAPI(title="PlasticSense API")

# enable CORS so the frontend can call the API from a different origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        return JSONResponse(
            status_code=500,
            content={
                "error": "ML service unavailable",
                "detail": detail,
            },
        )

    result = analyze_plastic(plastic_type)
    result["detected_by"] = "ML Image Analysis"
    return result