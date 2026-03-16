from typing import List
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup

from src.domain.entities import TrendingProject


class GitHubTrendingService:
    """负责抓取 GitHub Trending 页面并解析为领域实体。"""

    def __init__(self, base_url: str, since: str = "daily", timeout: int = 20) -> None:
        self.base_url = base_url
        self.since = since
        self.timeout = timeout

    def fetch_projects(self, limit: int = 10) -> List[TrendingProject]:
        """抓取并返回前 N 个热门项目。"""
        query = urlencode({"since": self.since})
        url = f"{self.base_url}?{query}"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
            )
        }
        response = requests.get(url, headers=headers, timeout=self.timeout)
        response.raise_for_status()
        return self._parse(response.text, limit=limit)

    def _parse(self, html: str, limit: int) -> List[TrendingProject]:
        soup = BeautifulSoup(html, "html.parser")
        articles = soup.select("article.Box-row")
        projects: List[TrendingProject] = []

        for article in articles[:limit]:
            title_el = article.select_one("h2 a")
            if not title_el:
                continue

            repo_path = " ".join(title_el.get_text(strip=True).split())
            repo_path = repo_path.replace(" / ", "/").replace(" ", "")
            repo_url = f"https://github.com/{repo_path}"

            description_el = article.select_one("p")
            description = description_el.get_text(" ", strip=True) if description_el else "暂无描述"

            language_el = article.select_one('[itemprop="programmingLanguage"]')
            language = language_el.get_text(strip=True) if language_el else None

            stars_today_el = article.select_one("span.d-inline-block.float-sm-right")
            stars_today = stars_today_el.get_text(" ", strip=True) if stars_today_el else None

            projects.append(
                TrendingProject(
                    name=repo_path,
                    url=repo_url,
                    description=description,
                    language=language,
                    stars_today=stars_today,
                )
            )

        return projects
