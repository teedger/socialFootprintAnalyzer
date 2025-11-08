# Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Option 1: Using the startup script (Recommended)

```bash
chmod +x run.sh
./run.sh
```

### Option 2: Manual setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up environment
cp .env.example .env

# 3. (Optional) Edit .env with your API keys
nano .env

# 4. Run the application
python main.py
```

### Option 3: Using uvicorn directly

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## 📝 First Run

1. Open your browser to http://localhost:8000
2. Enter a well-known name (e.g., "Elon Musk", "Microsoft", "OpenAI")
3. Click "Analyze Social Footprint"
4. View your results!

## ⚙️ API Keys (Optional but Recommended)

The app works without API keys in demo mode, but for full functionality:

### Get OpenAI API Key (for AI recommendations)
1. Visit https://platform.openai.com/
2. Sign up / Log in
3. Go to API Keys
4. Create new key
5. Add to `.env`: `OPENAI_API_KEY=sk-...`

### Get Google Search API (for web search)
1. Visit https://console.cloud.google.com/
2. Create project
3. Enable Custom Search API
4. Create API key
5. Create search engine at https://programmablesearchengine.google.com/
6. Add to `.env`:
   ```
   GOOGLE_API_KEY=your_key
   GOOGLE_SEARCH_ENGINE_ID=your_id
   ```

### Get NewsAPI (for news articles)
1. Visit https://newsapi.org/
2. Sign up
3. Copy API key
4. Add to `.env`: `NEWSAPI_KEY=your_key`

## 🎯 What Works Without API Keys?

- ✅ Basic web interface
- ✅ Mock data for demonstration
- ✅ All visualizations
- ✅ Rule-based recommendations
- ❌ Real Google search results
- ❌ Real news articles
- ❌ AI-powered recommendations

## 🔧 Troubleshooting

**Port 8000 already in use:**
```bash
# Change port in .env
echo "PORT=8001" >> .env
python main.py
```

**Dependencies not installing:**
```bash
# Try with sudo (not recommended) or use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**"Module not found" errors:**
```bash
# Make sure you're in the project directory
cd socialFootprintAnalyzer
pip install -r requirements.txt
```

## 📱 Testing the API

### Using curl:
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "Tesla"}'
```

### Using Python:
```python
import requests

response = requests.post(
    "http://localhost:8000/api/analyze",
    json={"query": "Tesla"}
)
print(response.json())
```

### Using the browser:
Visit http://localhost:8000/docs for interactive API documentation

## 🎨 Features to Try

1. **Search for a person**: "Bill Gates", "Taylor Swift"
2. **Search for a company**: "Apple", "Netflix"
3. **Search for yourself**: Your name or username
4. **View different metrics**: Visibility, Perception, Platform distribution
5. **Read recommendations**: AI-generated tips to improve
6. **Explore mentions**: Click through to original sources

## ⚡ Performance Tips

- First search may be slower (initializing models)
- Subsequent searches are faster
- With API keys: expect 5-15 seconds per analysis
- Without API keys: instant results (demo mode)

## 🔄 Updating

```bash
git pull
pip install -r requirements.txt --upgrade
python main.py
```

---

**Need help?** Check the full README.md or open an issue on GitHub!
