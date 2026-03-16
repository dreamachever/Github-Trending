import os


class Settings:
    """应用配置，统一从环境变量读取。"""

    @staticmethod
    def _get_int(name: str, default: int) -> int:
        raw = os.getenv(name, str(default))
        try:
            return int(raw)
        except (TypeError, ValueError):
            return default

    GITHUB_TRENDING_URL = os.getenv("GITHUB_TRENDING_URL", "https://github.com/trending")
    GITHUB_TRENDING_SINCE = os.getenv("GITHUB_TRENDING_SINCE", "daily")
    GITHUB_TRENDING_LIMIT = _get_int.__func__("GITHUB_TRENDING_LIMIT", 10)

    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    DEEPSEEK_TIMEOUT = _get_int.__func__("DEEPSEEK_TIMEOUT", 60)

    FEISHU_WEBHOOK_URL = os.getenv("FEISHU_WEBHOOK_URL", "")
    FEISHU_TIMEOUT = _get_int.__func__("FEISHU_TIMEOUT", 20)
