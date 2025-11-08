"""
Quick test to verify all imports work correctly
"""
import sys

def test_imports():
    print("Testing imports...")

    try:
        from config import Config
        print("✓ Config imported successfully")

        from backend.models.schemas import SearchRequest, AnalysisResult
        print("✓ Models imported successfully")

        from backend.services.data_aggregator import DataAggregator
        print("✓ DataAggregator imported successfully")

        from backend.services.ai_analyzer import AIAnalyzer
        print("✓ AIAnalyzer imported successfully")

        from backend.services.analyzer_service import AnalyzerService
        print("✓ AnalyzerService imported successfully")

        from backend.api.routes import router
        print("✓ API routes imported successfully")

        from main import app
        print("✓ FastAPI app imported successfully")

        print("\n✅ All imports successful!")
        print("\nConfiguration warnings:")
        warnings = Config.validate()
        for warning in warnings:
            print(f"  ⚠️  {warning}")

        if not warnings:
            print("  ✅ All API keys configured!")
        else:
            print("\n💡 The app will work in demo mode without API keys.")
            print("   For full functionality, add API keys to .env file.")

        return True

    except Exception as e:
        print(f"\n❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
