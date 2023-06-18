# AndyGPT Bot
![python-version](https://img.shields.io/badge/python-3.10-blue.svg)
[![openai-version](https://img.shields.io/badge/openai-0.27.8-orange.svg)](https://openai.com/)

A [Telegram bot](https://core.telegram.org/bots/api) that integrates with OpenAI's _official_ [ChatGPT](https://openai.com/blog/chatgpt/).

## Prerequisites
- Python 3.10+.
- A [Telegram bot](https://core.telegram.org/bots#6-botfather) and its token.
- An [OpenAI](https://openai.com) account and its token.

## Getting started

### Configuration
Customize the configuration by copying `.env.example` and renaming it to `.env`, then editing the required parameters as desired:

| Parameter                   | Description                                                                                                                                                                                                                   |
|-----------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `OPENAI_API_KEY`            | Your OpenAI API key, you can get it from [here](https://platform.openai.com/account/api-keys)                                                                                                                                 |
| `TELEGRAM_BOT_TOKEN`        | Your Telegram bot's token, obtained using [BotFather](http://t.me/botfather)

### Installing
#### From Source
1. Create a virtual environment:
```shell
python -m venv venv
```

2. Activate the virtual environment:
```shell
# For Linux or macOS:
source venv/bin/activate

# For Windows:
venv\Scripts\activate
```

3. Install the packages:
```shell
pip install -r requirements.txt
```

4. Start the bot:
```
python main.py
