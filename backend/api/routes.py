"""
API Routes for Social Footprint Analyzer
"""
from fastapi import APIRouter, HTTPException
from backend.models.schemas import SearchRequest, AnalysisResult
from backend.services.analyzer_service import AnalyzerService

router = APIRouter()
analyzer_service = AnalyzerService()


@router.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Social Footprint Analyzer API is running",
        "version": "1.0.0"
    }


@router.post("/analyze", response_model=AnalysisResult)
async def analyze_footprint(request: SearchRequest):
    """
    Analyze social footprint for a given query

    Parameters:
    - query: Name or organization to analyze

    Returns:
    - Complete analysis result with scores, sentiment, and recommendations
    """
    try:
        result = await analyzer_service.analyze_footprint(request.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }
