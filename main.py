import logging

from chatgpt import ChatGPTHelper
from bot import TelegramBot


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    chatgpt_helper = ChatGPTHelper()
    telegram_bot = TelegramBot(chatgpt_helper)
    telegram_bot.run()


if __name__ == '__main__':
    main()
