from src.config.settings import Settings
from src.services.deepseek_client import DeepSeekClient
from src.services.feishu_bot_client import FeishuBotClient
from src.services.github_trending_service import GitHubTrendingService
from src.usecases.daily_trending_report_usecase import DailyTrendingReportUseCase


def main() -> None:
    trending_service = GitHubTrendingService(
        base_url=Settings.GITHUB_TRENDING_URL,
        since=Settings.GITHUB_TRENDING_SINCE,
    )
    deepseek_client = DeepSeekClient(
        api_key=Settings.DEEPSEEK_API_KEY,
        base_url=Settings.DEEPSEEK_BASE_URL,
        model=Settings.DEEPSEEK_MODEL,
        timeout=Settings.DEEPSEEK_TIMEOUT,
    )
    feishu_client = FeishuBotClient(
        webhook_url=Settings.FEISHU_WEBHOOK_URL,
        timeout=Settings.FEISHU_TIMEOUT,
    )

    use_case = DailyTrendingReportUseCase(
        trending_service=trending_service,
        llm_client=deepseek_client,
        feishu_client=feishu_client,
    )
    digest = use_case.run(limit=Settings.GITHUB_TRENDING_LIMIT)
    print(f"日报发送成功: {digest.title}")


if __name__ == "__main__":
    main()
