from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from pipeline.pipeline import CNCPipeline
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# -------------------------------
# Request Model
# -------------------------------
class GCodeRequest(BaseModel):
    gcode: List[str]


# -------------------------------
# Initialize Pipeline
# -------------------------------
api_key = os.getenv("GROQ_API_KEY")
pipeline = CNCPipeline(api_key=api_key)


# -------------------------------
# Routes
# -------------------------------
@router.get("/")
def home():
    return {"message": "CNC AI Analyzer API is running 🚀"}


@router.post("/analyze")
def analyze_gcode(request: GCodeRequest):
    try:
        result = pipeline.run(request.gcode)

        return {
            "issues": [str(i) for i in result["issues"]],
            "metrics": result["metrics"],
            "ai": result["ai"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))