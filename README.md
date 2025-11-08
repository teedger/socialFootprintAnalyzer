# Social Footprint Analyzer

> **Analyze your online presence and discover how you're perceived across the web**

A powerful web application that analyzes social footprint and digital reputation by aggregating data from multiple online sources, performing AI-powered sentiment analysis, and providing actionable recommendations.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🌟 Features

### Core Capabilities

- **🔍 Multi-Source Data Aggregation**: Searches across Google, news sites, and social media platforms
- **📊 Visibility Scoring**: Calculates a 0-100 score based on online presence and platform diversity
- **😊 Sentiment Analysis**: AI-powered analysis of how you're perceived (positive, neutral, negative)
- **📈 Interactive Dashboard**: Beautiful visualizations with charts and graphs
- **🎯 AI Recommendations**: Personalized suggestions to improve your digital footprint
- **🔑 Keyword Extraction**: Identifies top themes and topics associated with your name
- **🌐 Platform Distribution**: See where you're most visible online

### User Experience

- Clean, responsive UI built with TailwindCSS
- Real-time progress feedback during analysis
- Interactive charts using Chart.js
- Mobile-friendly design
- Fast and efficient async data processing

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- API keys (optional, but recommended for full functionality)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/socialFootprintAnalyzer.git
cd socialFootprintAnalyzer
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure environment variables**

Copy the example env file and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# OpenAI (for AI recommendations)
OPENAI_API_KEY=your_openai_api_key_here

# Google Custom Search (for web search)
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here

# NewsAPI (for news articles)
NEWSAPI_KEY=your_newsapi_key_here

# Twitter/X API (optional)
TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here

# Reddit API (optional)
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
```

4. **Run the application**

```bash
python main.py
```

5. **Open your browser**

Navigate to: `http://localhost:8000`

---

## 🔑 Getting API Keys

### OpenAI API (Recommended)

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy and paste into `.env`

### Google Custom Search API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Custom Search API
4. Create credentials (API Key)
5. Create a Custom Search Engine at [Programmable Search Engine](https://programmablesearchengine.google.com/)
6. Copy both the API key and Search Engine ID

### NewsAPI

1. Go to [NewsAPI.org](https://newsapi.org/)
2. Sign up for a free account
3. Copy your API key from the dashboard

### Twitter/Reddit (Optional)

- **Twitter**: [Twitter Developer Portal](https://developer.twitter.com/)
- **Reddit**: [Reddit Apps](https://www.reddit.com/prefs/apps)

---

## 📁 Project Structure

```
socialFootprintAnalyzer/
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py           # API endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py          # Data models (Pydantic)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── data_aggregator.py  # Data collection from APIs
│   │   ├── ai_analyzer.py      # AI/NLP analysis
│   │   └── analyzer_service.py # Main orchestration service
│   └── __init__.py
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css       # Custom styles
│   │   ├── js/
│   │   │   └── app.js          # Frontend logic
│   │   └── images/
│   └── templates/
│       └── index.html          # Main HTML template
├── config.py                   # Configuration management
├── main.py                     # FastAPI application entry point
├── requirements.txt            # Python dependencies
├── .env.example               # Example environment variables
└── README.md                  # This file
```

---

## 🔧 Configuration

### Application Settings

Edit `config.py` or use environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `True` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `MAX_SEARCH_RESULTS` | Max results per source | `50` |
| `SENTIMENT_THRESHOLD_POSITIVE` | Positive sentiment threshold | `0.1` |
| `SENTIMENT_THRESHOLD_NEGATIVE` | Negative sentiment threshold | `-0.1` |

---

## 📡 API Documentation

### Endpoints

#### `POST /api/analyze`

Analyze social footprint for a given query.

**Request Body:**
```json
{
  "query": "Elon Musk"
}
```

**Response:**
```json
{
  "query": "Elon Musk",
  "visibility_score": 95,
  "perception_score": 72,
  "total_mentions": 42,
  "sentiment_breakdown": {
    "positive": 18,
    "neutral": 15,
    "negative": 9,
    "positive_percent": 42.9,
    "neutral_percent": 35.7,
    "negative_percent": 21.4
  },
  "platform_distribution": [
    {
      "platform": "News",
      "count": 20,
      "percentage": 47.6
    }
  ],
  "top_mentions": [...],
  "keywords": ["tesla", "spacex", "twitter"],
  "recommendations": [
    "Continue engaging professionally on LinkedIn",
    "Address negative mentions proactively"
  ],
  "analyzed_at": "2024-01-15T10:30:00"
}
```

#### `GET /api/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00"
}
```

### Interactive API Docs

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 🎯 How It Works

### Analysis Pipeline

1. **Data Collection**
   - Searches Google for web mentions
   - Queries NewsAPI for articles
   - Scans social media platforms
   - Aggregates all results

2. **Sentiment Analysis**
   - Uses TextBlob for natural language processing
   - Classifies each mention as positive, neutral, or negative
   - Calculates overall sentiment distribution

3. **Score Calculation**
   - **Visibility Score**: Based on mention count, platform diversity, and source quality
   - **Perception Score**: Derived from sentiment analysis (50 = neutral, 100 = all positive)

4. **Keyword Extraction**
   - Analyzes all text snippets
   - Identifies most common themes and topics
   - Returns top keywords

5. **AI Recommendations**
   - Uses OpenAI GPT-3.5 for intelligent suggestions
   - Falls back to rule-based logic if API unavailable
   - Provides 3-5 actionable recommendations

6. **Visualization**
   - Renders interactive charts
   - Displays platform distribution
   - Shows sentiment breakdown

---

## 🧪 Development

### Running in Development Mode

```bash
# With auto-reload
uvicorn main:app --reload --port 8000

# Or use the main.py script
python main.py
```

### Testing

The app will work with or without API keys, but functionality is limited:

- **Without API keys**: Demo mode with mock data
- **With OpenAI**: AI-powered recommendations
- **With Google/News APIs**: Real web data
- **Full setup**: Complete functionality

### Adding New Data Sources

To add a new platform:

1. Create a method in `backend/services/data_aggregator.py`
2. Add API call logic
3. Append results to `self.results`
4. Include in the `aggregate()` method

Example:
```python
async def search_new_platform(self, query: str) -> None:
    # Your API logic here
    results = await fetch_from_platform(query)
    for item in results:
        self.results.append({
            "platform": "NewPlatform",
            "title": item.title,
            "url": item.url,
            "snippet": item.description,
            "date": item.date
        })
```

---

## 🎨 Customization

### Styling

Edit `frontend/static/css/style.css` to customize:
- Colors and themes
- Animations
- Typography
- Responsive breakpoints

### Scoring Algorithm

Modify scoring logic in `backend/services/ai_analyzer.py`:
- `calculate_visibility_score()`: Adjust weights for mentions, diversity, quality
- `calculate_perception_score()`: Change sentiment weighting

---

## 🐛 Troubleshooting

### Common Issues

**"Analysis failed" error**
- Check that your API keys are correctly set in `.env`
- Ensure all dependencies are installed
- Check console/terminal for detailed error messages

**No results or low scores**
- Try a more well-known name/organization for testing
- Check API rate limits (especially for free tiers)
- Verify API keys have correct permissions

**Charts not displaying**
- Ensure JavaScript is enabled
- Check browser console for errors
- Try clearing cache and refreshing

**Port already in use**
- Change the `PORT` in `.env` or config.py
- Or kill the process using port 8000: `lsof -ti:8000 | xargs kill`

---

## 📊 Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **aiohttp**: Async HTTP client
- **BeautifulSoup4**: Web scraping
- **TextBlob**: NLP and sentiment analysis
- **OpenAI**: AI-powered recommendations

### Frontend
- **TailwindCSS**: Utility-first CSS framework
- **Chart.js**: Interactive charts
- **Vanilla JavaScript**: No heavy frameworks needed
- **Jinja2**: Template engine

### APIs & Services
- Google Custom Search API
- NewsAPI
- OpenAI API
- Twitter API (optional)
- Reddit API (optional)

---

## 🚧 Roadmap (Phase 2)

- [ ] User authentication and saved searches
- [ ] Compare multiple entities side-by-side
- [ ] Historical tracking and trend analysis
- [ ] Email alerts for new mentions
- [ ] PDF report generation
- [ ] More social platforms (Instagram, LinkedIn, TikTok)
- [ ] Advanced filtering and date ranges
- [ ] Competitor benchmarking
- [ ] Chrome extension
- [ ] Mobile app

---

## 👥 Target Audience

- **Professionals**: Monitor personal brand and reputation
- **Companies**: Track online presence and sentiment
- **Job Seekers**: Understand how employers might see them
- **Recruiters**: Research candidates
- **PR/Marketing Teams**: Measure campaign impact
- **Researchers**: Study public perception

---

## 📄 License

MIT License - feel free to use this project for personal or commercial purposes.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review API documentation

---

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Styled with [TailwindCSS](https://tailwindcss.com/)
- Charts powered by [Chart.js](https://www.chartjs.org/)
- AI by [OpenAI](https://openai.com/)

---

**Made with ❤️ for understanding your digital footprint**
