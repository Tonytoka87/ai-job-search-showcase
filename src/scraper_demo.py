"""
scraper_demo.py
Generic architectural example of the hybrid scraping approach used in the project.
This script demonstrates how free HTML parsing is used as a "gatekeeper" before
querying an expensive API.
"""

import requests
import re
from typing import List, Dict
from bs4 import BeautifulSoup

# Example generic settings
FIRECRAWL_API_URL = "https://api.firecrawl.dev/v1/scrape"
HEADERS = {"User-Agent": "Mozilla/5.0 ..."}
VALID_LOCATIONS = ["oslo", "skøyen", "lysaker"]

class CloudScraper:
    def __init__(self, api_key: str):
        self.firecrawl_api_key = api_key
        self.credits_used = 0
        self.max_credits = 50

    def _is_location_relevant(self, location_text: str) -> bool:
        """Rule-based filtering to ensure jobs fit the physical criteria."""
        if not location_text:
            return True
        loc = location_text.lower()
        return any(valid in loc for valid in VALID_LOCATIONS)

    def _search_free_tier(self, keyword: str) -> List[Dict]:
        """
        Uses BeautifulSoup to scrape metadata (title, URL, location)
        from job boards WITHOUT consuming API credits.
        """
        url = f"https://example.com/jobs?q={keyword}"
        response = requests.get(url, headers=HEADERS, timeout=15)
        
        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        for a in soup.find_all("a", class_="job-link"):
            results.append({
                "url": a["href"],
                "title": a.get_text(strip=True),
                "location": a.get("data-location", "Unknown")
            })
        return results

    def _fetch_full_content(self, url: str) -> str:
        """
        Uses Firecrawl API to extract raw markdown from the job posting,
        consumes 1 credit per call.
        """
        if self.credits_used >= self.max_credits:
            return ""

        self.credits_used += 1
        headers = {"Authorization": f"Bearer {self.firecrawl_api_key}"}
        payload = {"url": url, "formats": ["markdown"], "onlyMainContent": True}
        
        response = requests.post(FIRECRAWL_API_URL, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("data", {}).get("markdown", "")
        return ""

    def run(self, keywords: List[str]):
        """Main orchestrator function."""
        for keyword in keywords:
            # 1. Gatekeeper step (Free)
            results = self._search_free_tier(keyword)
            
            for job in results:
                # 2. Heuristic filtering validation
                if not self._is_location_relevant(job["location"]):
                    continue
                
                # 3. Deep extraction (Paid API)
                content = _fetch_full_content(job["url"])
                if content:
                    # 4. Save to Database (e.g., Supabase payload generation)
                    print(f"Processed: {job['title']} (URL: {job['url']})")

if __name__ == "__main__":
    scraper = CloudScraper("api-key-placeholder")
    scraper.run(["AI Architect", "Prompt Engineer"])
