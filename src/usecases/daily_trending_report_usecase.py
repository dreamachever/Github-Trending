import re
from datetime import datetime
from typing import List

from src.domain.entities import DailyDigest, TrendingProject
from src.services.deepseek_client import DeepSeekClient
from src.services.feishu_bot_client import FeishuBotClient
from src.services.github_trending_service import GitHubTrendingService


class DailyTrendingReportUseCase:
    """Daily flow: fetch -> summarize -> send."""

    def __init__(
        self,
        trending_service: GitHubTrendingService,
        llm_client: DeepSeekClient,
        feishu_client: FeishuBotClient,
    ) -> None:
        self.trending_service = trending_service
        self.llm_client = llm_client
        self.feishu_client = feishu_client

    def run(self, limit: int) -> DailyDigest:
        projects = self.trending_service.fetch_projects(limit=limit)
        if not projects:
            raise RuntimeError("No GitHub Trending projects fetched.")

        summary = self.llm_client.summarize_projects(projects)
        digest = self._build_digest(summary=summary, projects=projects)
        self.feishu_client.send_markdown(title=digest.title, content=digest.content)
        return digest

    @staticmethod
    def _build_digest(summary: str, projects: List[TrendingProject]) -> DailyDigest:
        date_text = datetime.now().strftime("%Y-%m-%d")
        title = f"GitHub Trending 日报 - {date_text}"

        # Remove markdown markers to keep Feishu output plain text.
        clean_summary = DailyTrendingReportUseCase._strip_markdown(summary)
        project_index = "\n".join([f"{i}. {p.name} - {p.url}" for i, p in enumerate(projects, start=1)])
        content = f"{title}\n\n{clean_summary}\n\n项目索引:\n{project_index}"
        return DailyDigest(title=title, content=content)

    @staticmethod
    def _strip_markdown(text: str) -> str:
        cleaned = text
        cleaned = re.sub(r"^\s{0,3}#{1,6}\s*", "", cleaned, flags=re.MULTILINE)
        cleaned = re.sub(r"\*\*(.*?)\*\*", r"\1", cleaned)
        cleaned = re.sub(r"\*(.*?)\*", r"\1", cleaned)
        cleaned = re.sub(r"`{1,3}", "", cleaned)
        cleaned = re.sub(r"^\s*[-*_]{3,}\s*$", "", cleaned, flags=re.MULTILINE)
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
        return cleaned.strip()
