from dataclasses import dataclass
from typing import Optional


@dataclass
class TrendingProject:
    """GitHub Trending 项目信息实体。"""

    name: str
    url: str
    description: str
    language: Optional[str] = None
    stars_today: Optional[str] = None


@dataclass
class DailyDigest:
    """日报内容实体。"""

    title: str
    content: str
