from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

# import from the package context
from decision_engine import analyze_plastic
from ml.model import predict_plastic_type
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
    plastic_type = predict_plastic_type(file.file)
    result = analyze_plastic(plastic_type)
    result["detected_by"] = "ML Image Analysis"
    return result