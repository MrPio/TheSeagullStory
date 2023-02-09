"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import __version__ as TG_VER

from managers.answer_manager import AnswerManager
from managers.tag_manager import TagManager

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 5):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [[
        "/help",
        "Was Albert at the pier because he was lost?",
        "Were there more than 3 persons on the boat?",
        "Were there more than 1 persons on the boat?",
    ],
    [
        "Were there more than 3 persons at the restaurant?",
        "Was the seagull edible?"
    ]]

    await update.message.reply_text(
        "⛵ Welcome to the seagull story! ⛵\n\n"
        "In this game I describe you a strange episode and you need to find out the meaning of this story asking me only yes/no question. ",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=False, input_field_placeholder="Here your question...", is_persistent=True
        ),
    )


async def question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply = ['No', 'Yes', 'Doesn\'t matter']

    user = update.message.from_user
    print(f'user: {user.username}, full name: {user.full_name}')

    question = update.message.text
    print(question)
    tag = TagManager.get_instance().ask(question)
    answer = AnswerManager.get_instance().answer(question, tag)
    await update.message.reply_text(reply[answer])


def main() -> None:
    application = Application.builder().token("6059753686:AAErerWq6WZ2K18E-ojOZ4wl-xGmpGsztg8").build()

    help_handler = CommandHandler('help', help)
    question_handler = MessageHandler(filters.TEXT, question)

    application.add_handler(help_handler)
    application.add_handler(question_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
