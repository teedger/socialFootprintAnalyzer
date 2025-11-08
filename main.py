"""
Main FastAPI Application
Social Footprint Analyzer
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router
from config import Config

# Initialize FastAPI app
app = FastAPI(
    title="Social Footprint Analyzer",
    description="Analyze online presence and social footprint",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Configure templates
templates = Jinja2Templates(directory="frontend/templates")

# Include API routes
app.include_router(router, prefix="/api", tags=["api"])


@app.get("/")
async def home(request: Request):
    """Render the home page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.on_event("startup")
async def startup_event():
    """Application startup"""
    print("🚀 Social Footprint Analyzer starting...")

    # Validate configuration
    warnings = Config.validate()
    if warnings:
        print("⚠️  Configuration warnings:")
        for warning in warnings:
            print(f"   - {warning}")

    print(f"✅ Server running at http://{Config.HOST}:{Config.PORT}")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown"""
    print("👋 Social Footprint Analyzer shutting down...")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=Config.DEBUG
    )
