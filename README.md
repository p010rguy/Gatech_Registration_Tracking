# Gatech Registration Tracking

[中文](#中文) | [EN](#en)

Polls the Georgia Tech Banner public search API to monitor seat availability for selected courses and sends email alerts when seats open.

## Features
- Poll course seat availability
- Send Gmail alerts when seats open
- Cool down for 5 minutes after sending, then resume monitoring
- Quit by typing `q` and pressing Enter (or Ctrl+C)
- Built-in retry with backoff for HTTP/SMTP

## 中文

通过轮询 Georgia Tech Banner 公开检索接口监控课程余量，并在有空位时发送邮件提醒。

## 功能
- 轮询课程席位信息
- 有空位时发送 Gmail 提醒邮件
- 发送后进入 5 分钟冷却，再继续监控
- 输入 `q` 回车退出（或 Ctrl+C）
- HTTP/SMTP 自动重试与退避

## EN

## Requirements
- Python 3.11+
- Dependencies: `requests`, `beautifulsoup4`

## 环境要求
- Python 3.11+
- 依赖库：`requests`、`beautifulsoup4`

## Install
Install `uv`:
```bash
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
```
```bash
# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Official site: https://astral.sh/uv/

Sync dependencies:
```bash
uv sync
```

## 安装依赖
先安装 `uv`：
```bash
# macOS 和 Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```
```bash
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
官方链接：https://astral.sh/uv/

使用 `uv` 同步依赖：
```bash
uv sync
```

## Configuration
Edit `main.py`:

1) Course mapping (CRN -> (subject, courseNumber)):
```python
course = {
    35419: 6239,
    35418: 6252,
}
classSubject = ["CS", "ECE"]
```
CS 6270, ECE 6239, ECE 6252


2) Term:
```python
term = "202602"
```

3) Email credentials:
```python
sender = "your_email@gmail.com"
receiver = "your_email@gmail.com"
password = "your_app_password"
```
Use a Gmail App Password, not your regular login password.
Enter App password here. Link to get app password: https://myaccount.google.com/apppasswords

4) Poll/timeout/retry tuning (optional):
```python
TIMEOUT_SECONDS = 12
MAX_RETRIES = 4
BACKOFF_SECONDS = 1.5
```

5) Cooldown and update rate (optional):
```python
re_add_course_duration = 300
update_rate = 5
```

## 配置
在 `main.py` 中修改以下配置：

1) 课程映射（CRN -> (subject, courseNumber)）：
```python
course = {
    35419: 6239,
    35418: 6252,
    34931: 6270
}
classSubject = ["CS", "ECE"]
```
CS 6270, ECE 6239, ECE 6252

2) 学期：
```python
term = "202602"
```

3) 邮件账号：
```python
sender = "your_email@gmail.com"
receiver = "your_email@gmail.com"
password = "your_app_password"
```
说明：请使用 Gmail App Password，不要使用邮箱登录密码。
Enter App password here. Link to get app password: https://myaccount.google.com/apppasswords

4) 轮询频率/超时/重试（可选）：
```python
TIMEOUT_SECONDS = 12
MAX_RETRIES = 4
BACKOFF_SECONDS = 1.5
```

5) 冷却与轮询频率（可选）：
```python
re_add_course_duration = 300
update_rate = 5
```

## Run
```bash
uv run main.py
```

Example output:
```
[2026-01-16 08:17:53] 35419 : 0
```

## 运行
```bash
uv run main.py
```

示例输出：
```
[2026-01-16 08:17:53] 35419 : 0
```

## Quit
- Type `q` and press Enter
- Or Ctrl+C

## 退出
- 输入 `q` 回车退出
- 或 Ctrl+C

## Troubleshooting
1) Request timeout / RemoteDisconnected
- Usually rate limiting or unstable network; retry/backoff is already enabled.
- Increase `TIMEOUT_SECONDS` or reduce polling frequency (`time.sleep`).

2) Gmail send failures (451/timeout)
- Usually connection timeout or throttling; email send already retries with new connections.
- Increase `SMTP_TIMEOUT_SECONDS` or reduce send frequency.

## 常见问题
1) 请求超时 / RemoteDisconnected
- 可能被限流或网络不稳，已内置重试与退避。
- 可适当提高 `TIMEOUT_SECONDS` 或降低轮询频率（`time.sleep`）。

2) Gmail 发送失败 (451/timeout)
- 可能是连接超时或限流，邮件发送已改为每次新建连接并重试。
- 可提高 `SMTP_TIMEOUT_SECONDS` 或降低发送频率。

## Disclaimer
This script uses a public search interface. Use it in compliance with Georgia Tech policies and terms of service.

## 免责声明
该脚本调用的是公开检索接口，请确保使用符合学校政策与服务条款。
