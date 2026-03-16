# GitHub Trending Daily Bot

每天自动抓取 GitHub Trending，调用 DeepSeek 生成总结，并发送到飞书群机器人。

## 架构设计（面向对象 + 分层）

- `domain`：核心实体对象（`TrendingProject`、`DailyDigest`）
- `services`：外部系统适配层
- `usecases`：业务编排层（抓取 -> 总结 -> 推送）
- `main.py`：应用入口

## 快速开始

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 配置环境变量（可复制 `.env.example`）

- `DEEPSEEK_API_KEY`：DeepSeek API Key
- `FEISHU_WEBHOOK_URL`：飞书群机器人 Webhook

3. 本地运行

```bash
python -m src.main
```

## GitHub Actions 定时任务

工作流文件：`.github/workflows/daily-trending.yml`

- 每天 UTC `01:00` 触发（北京时间 `09:00`）
- 也支持手动触发 `workflow_dispatch`

请在仓库 `Settings -> Secrets and variables -> Actions` 中配置：

- `DEEPSEEK_API_KEY`
- `FEISHU_WEBHOOK_URL`
- 可选：`GITHUB_TRENDING_LIMIT`、`DEEPSEEK_MODEL` 等

## 说明

- 若未配置 `DEEPSEEK_API_KEY`，程序会输出规则化简版摘要，保证链路可验证。
- 若 `FEISHU_WEBHOOK_URL` 未配置，发送阶段会报错并退出。
