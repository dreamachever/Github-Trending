from typing import List

import requests

from src.domain.entities import TrendingProject


class DeepSeekClient:
    """DeepSeek API client (chat completions)."""

    def __init__(self, api_key: str, base_url: str, model: str, timeout: int = 60) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def summarize_projects(self, projects: List[TrendingProject]) -> str:
        """Call LLM and return a Chinese summary."""
        if not self.api_key:
            return self._fallback_summary(projects)

        prompt = self._build_prompt(projects)
        endpoint = f"{self.base_url}/chat/completions"
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "你是资深技术情报分析师，擅长给工程团队写简洁日报。"},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.3,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        response = requests.post(endpoint, json=payload, headers=headers, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

    def _build_prompt(self, projects: List[TrendingProject]) -> str:
        lines = []
        for idx, project in enumerate(projects, start=1):
            lines.append(
                (
                    f"{idx}. {project.name}\n"
                    f"   URL: {project.url}\n"
                    f"   描述: {project.description}\n"
                    f"   语言: {project.language or '未知'}\n"
                    f"   今日增星: {project.stars_today or '未知'}"
                )
            )

        project_text = "\n".join(lines)
        return (
            "请根据以下 GitHub Trending 项目生成中文日报。\n"
            "要求:\n"
            "1. 开头给 3 到 5 条趋势洞察。\n"
            "2. 每个项目用 1 到 2 句话说明价值和适用场景。\n"
            "3. 最后给团队 3 条可执行建议。\n"
            "4. 输出为纯文本，不要使用 Markdown，不要出现 #、*、- 这类格式符号。\n\n"
            f"{project_text}"
        )

    @staticmethod
    def _fallback_summary(projects: List[TrendingProject]) -> str:
        """Fallback summary when API key is missing."""
        lines = ["今日 GitHub Trending（简版）", ""]
        for project in projects:
            lines.append(
                f"{project.name} ({project.language or '未知语言'})：{project.description}  链接: {project.url}"
            )
        lines.append("")
        lines.append("未检测到 DeepSeek API Key，以上为基础汇总。")
        return "\n".join(lines)
