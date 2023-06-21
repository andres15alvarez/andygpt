import asyncio
import logging
from telegram import Message, MessageEntity, Update, constants
from telegram.ext import CallbackContext, ContextTypes


def message_text(message: Message) -> str:
    """Returns the text of a message, excluding any bot commands."""
    message_txt = message.text
    if message_txt is None:
        return ''

    for _, text in sorted(message.parse_entities([MessageEntity.BOT_COMMAND]).items(),
                          key=(lambda item: item[0].offset)):
        message_txt = message_txt.replace(text, '').strip()

    return message_txt if len(message_txt) > 0 else ''


def get_thread_id(update: Update) -> int | None:
    """Gets the message thread id for the update, if any."""
    if update.effective_message and update.effective_message.is_topic_message:
        return update.effective_message.message_thread_id
    return None


def split_into_chunks(text: str, chunk_size: int = 4096) -> list[str]:
    """Splits a string into chunks of a given size."""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


async def wrap_with_indicator(
    update: Update,
    context: CallbackContext,
    coroutine,
    chat_action: constants.ChatAction = "",
    is_inline=False
):
    """Wraps a coroutine while repeatedly sending a chat action to the user."""
    task = context.application.create_task(coroutine(), update=update)
    while not task.done():
        if not is_inline:
            context.application.create_task(
                update.effective_chat.send_action(
                    chat_action,
                    message_thread_id=get_thread_id(update)
                )
            )
        try:
            await asyncio.wait_for(asyncio.shield(task), 4.5)
        except asyncio.TimeoutError:
            pass


async def error_handler(_: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles errors in the telegram-python-bot library."""
    logging.error(f'Exception while handling an update: {context.error}')


def get_reply_to_message_id(enable_quoting: bool, update: Update) -> int:
    """Returns the message id of the message to reply to.

    Args:
        - enable_quoting (bool): If quoting is enable
        - update (Update): Telegram update object

    Returns:
        - (int): Message id of the message to reply to,
        or None if quoting is disabled.
    """
    if enable_quoting:
        return update.message.message_id
    return None
