import os
from dotenv import load_dotenv


load_dotenv()

OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

PROXY = os.getenv('PROXY', None)

N_CHOICES = int(os.getenv('N_CHOICES', 1))

TEMPERATURE = float(os.getenv('TEMPERATURE', 1.0))

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

ENABLE_QUOTING = os.getenv('ENABLE_QUOTING', 'true').lower() == 'true'
