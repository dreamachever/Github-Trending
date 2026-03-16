import requests


class FeishuBotClient:
    """飞书群机器人客户端（Webhook）。"""

    def __init__(self, webhook_url: str, timeout: int = 20) -> None:
        self.webhook_url = webhook_url
        self.timeout = timeout

    def send_markdown(self, title: str, content: str) -> None:
        if not self.webhook_url:
            raise ValueError("FEISHU_WEBHOOK_URL 未配置。")

        payload = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": title,
                        "content": [
                            [
                                {
                                    "tag": "text",
                                    "text": content,
                                }
                            ]
                        ],
                    }
                }
            },
        }
        response = requests.post(self.webhook_url, json=payload, timeout=self.timeout)
        response.raise_for_status()
