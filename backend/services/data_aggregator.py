"""
Data Aggregation Service
Collects data from various sources: Google Search, News, Social Media
"""
import asyncio
import aiohttp
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import requests
from config import Config


class DataAggregator:
    """Aggregates data from multiple online sources"""

    def __init__(self):
        self.config = Config()
        self.results = []

    async def aggregate(self, query: str) -> List[Dict]:
        """
        Main aggregation method - collects data from all sources
        """
        self.results = []

        # Run all data collection tasks concurrently
        tasks = [
            self.search_google(query),
            self.search_news(query),
            self.search_social_media(query)
        ]

        await asyncio.gather(*tasks, return_exceptions=True)

        return self.results

    async def search_google(self, query: str) -> None:
        """Search Google using Custom Search API"""
        if not self.config.GOOGLE_API_KEY or not self.config.GOOGLE_SEARCH_ENGINE_ID:
            print("Google API not configured, skipping...")
            return

        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                "key": self.config.GOOGLE_API_KEY,
                "cx": self.config.GOOGLE_SEARCH_ENGINE_ID,
                "q": query,
                "num": 10
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        items = data.get("items", [])

                        for item in items:
                            self.results.append({
                                "platform": "Google Search",
                                "title": item.get("title", ""),
                                "url": item.get("link", ""),
                                "snippet": item.get("snippet", ""),
                                "date": None
                            })
        except Exception as e:
            print(f"Error searching Google: {e}")

    async def search_news(self, query: str) -> None:
        """Search news articles using NewsAPI"""
        if not self.config.NEWSAPI_KEY:
            print("NewsAPI not configured, skipping...")
            return

        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                "apiKey": self.config.NEWSAPI_KEY,
                "q": query,
                "sortBy": "relevancy",
                "pageSize": 20,
                "language": "en"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        articles = data.get("articles", [])

                        for article in articles:
                            self.results.append({
                                "platform": "News",
                                "title": article.get("title", ""),
                                "url": article.get("url", ""),
                                "snippet": article.get("description", ""),
                                "date": article.get("publishedAt", None)
                            })
        except Exception as e:
            print(f"Error searching news: {e}")

    async def search_social_media(self, query: str) -> None:
        """
        Search social media platforms
        Note: This is a simplified version. In production, you'd use official APIs
        """
        # Add mock social media results for demonstration
        # In production, implement actual API calls to Twitter, Reddit, LinkedIn, etc.

        mock_platforms = ["LinkedIn", "Twitter/X", "Reddit", "Instagram"]

        for platform in mock_platforms:
            # This is mock data - replace with actual API calls
            self.results.append({
                "platform": platform,
                "title": f"{query} mentioned on {platform}",
                "url": f"https://{platform.lower().replace('/', '')}.com/search?q={query.replace(' ', '+')}",
                "snippet": f"Profile or mentions of {query} found on {platform}",
                "date": None
            })

    async def search_reddit(self, query: str) -> None:
        """Search Reddit using PRAW"""
        if not self.config.REDDIT_CLIENT_ID or not self.config.REDDIT_CLIENT_SECRET:
            return

        try:
            # Reddit API implementation
            # This would use PRAW (Python Reddit API Wrapper)
            pass
        except Exception as e:
            print(f"Error searching Reddit: {e}")

    async def search_twitter(self, query: str) -> None:
        """Search Twitter/X using API v2"""
        if not self.config.TWITTER_BEARER_TOKEN:
            return

        try:
            # Twitter API implementation
            # This would use Tweepy
            pass
        except Exception as e:
            print(f"Error searching Twitter: {e}")

    def scrape_webpage(self, url: str) -> Optional[str]:
        """
        Scrape additional content from a webpage
        Used for enhanced analysis
        """
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Extract text content
                text = soup.get_text()
                return text[:1000]  # Limit to first 1000 chars
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None
