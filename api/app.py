from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="CNC AI Analyzer API",
    description="API for G-code analysis, debugging, optimization",
    version="1.0"
)

app.include_router(router)