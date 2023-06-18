import logging
from telegram import Update, constants
from telegram import BotCommand
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    Application,
    ContextTypes,
    filters
)

from utils import (
    get_thread_id,
    message_text,
    wrap_with_indicator,
    split_into_chunks,
    get_reply_to_message_id,
    error_handler
)
from chatgpt import ChatGPTHelper
from config import TELEGRAM_BOT_TOKEN, PROXY, ENABLE_QUOTING


class TelegramBot:
    """
    Class representing a ChatGPT Telegram Bot.
    """

    def __init__(self, chatgpt_helper: ChatGPTHelper):
        """Init the bot with the GPT helper.

        Args:
            - chatgpt_helper ChatGPTHelper: object
        """
        self.chatgpt = chatgpt_helper
        self.commands = [
            BotCommand(command='help', description="Muestra el mensaje de ayuda"),
        ]

    async def help(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        """Shows the help menu."""
        commands_description = [
            f'/{command.command} - {command.description}'
            for command in self.commands
        ]
        help_text = (
                'Soy un bot de ChatGPT, ¡háblame!' +
                '\n\n' +
                '\n'.join(commands_description)
        )
        await update.message.reply_text(help_text, disable_web_page_preview=True)

    async def prompt(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """React to incoming messages and respond accordingly."""
        if update.edited_message or not update.message or update.message.via_bot:
            return

        logging.info(
            f'New message received from user {update.message.from_user.name}'
        )
        prompt = message_text(update.message)

        async def _reply():
            response = await self.chatgpt.get_chat_response(prompt)
            chunks = split_into_chunks(response)
            for index, chunk in enumerate(chunks):
                await update.effective_message.reply_text(
                    message_thread_id=get_thread_id(update),
                    reply_to_message_id=update.message.message_id if index == 0 else None,
                    text=chunk
                )
        try:
            await wrap_with_indicator(
                update,
                context,
                _reply,
                constants.ChatAction.TYPING
            )
        except Exception as e:
            logging.exception(e)
            await update.effective_message.reply_text(
                message_thread_id=get_thread_id(update),
                reply_to_message_id=get_reply_to_message_id(ENABLE_QUOTING, update),
                text=f"No se pudo obtener la respuesta {str(e)}"
            )

    async def post_init(self, application: Application) -> None:
        """Post initialization hook for the bot."""
        await application.bot.set_my_commands(self.commands)

    def run(self):
        """Runs the bot."""
        application = ApplicationBuilder() \
            .token(TELEGRAM_BOT_TOKEN) \
            .proxy_url(PROXY) \
            .get_updates_proxy_url(PROXY) \
            .post_init(self.post_init) \
            .concurrent_updates(True) \
            .build()

        application.add_handler(CommandHandler('help', self.help))
        application.add_handler(CommandHandler('start', self.help))
        application.add_handler(CommandHandler(
            'chat',
            self.prompt,
            filters=filters.ChatType.GROUP | filters.ChatType.SUPERGROUP
        ))
        application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.prompt))
        application.add_error_handler(error_handler)
        application.run_polling()
