import logging
from enum import Enum

from environs import Env
from notifiers.logging import NotificationHandler
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, \
    ConversationHandler, RegexHandler

from format_answer import format_answer
from redis_tools import auth_redis, get_random_question, set_user_question, \
    get_user_question, get_answer

logger = logging.getLogger(__name__)


class QuizStates(Enum):
    CHOOSING = 0


def start(bot, update):
    """Send a message when the command /start is issued."""
    custom_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счет']]
    update.message.reply_text(
        text="Добро пожаловать на онлайн-викторину.\n \
        Нажми 'Новый вопрос' чтобы начать игру",
        reply_markup=ReplyKeyboardMarkup(custom_keyboard))
    return QuizStates.CHOOSING


def handle_new_question_request(bot, update):
    question = get_random_question(quiz_db)
    set_user_question(quiz_db, update.effective_user.id, question)
    update.message.reply_text(question)


def handle_solution_attempt(bot, update):
    question = get_user_question(quiz_db, update.effective_user.id)
    answer = format_answer(get_answer(quiz_db, question))
    user_answer = format_answer(update.message.text)
    if (user_answer in answer) and (len(answer) * 0.25 < len(user_answer)):
        update.message.reply_text(
            "Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос")
    else:
        update.message.reply_text("Неправильно… Попробуешь ещё раз?")


def handle_give_up(bot, update):
    question = get_user_question(quiz_db, update.effective_user.id)
    answer = get_answer(quiz_db, question)
    update.message.reply_text(f"Правильный ответ: {answer}")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning(f'Update "{update}" caused error "{error}"')


def cancel(bot, update):
    user = update.message.from_user
    logger.info(f"User {user.first_name} canceled the conversation.")
    update.message.reply_text('Пока. Увидимся в следующий раз.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def main():
    logging.basicConfig(
        format='%(asctime)s : %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S',
        level=logging.INFO
    )
    env = Env()
    env.read_env()
    telegram_api_token = env("TELEGRAM_API_TOKEN")
    telegram_chat_id = env("TELEGRAM_CHAT_ID")
    redis_address = env("REDIS_ADDRESS")
    redis_port = env("REDIS_PORT")
    redis_password = env("REDIS_PASSWORD")

    global quiz_db
    quiz_db = auth_redis(redis_address, redis_port, redis_password)

    params = {
        'token': telegram_api_token,
        'chat_id': telegram_chat_id
    }
    tg_handler = NotificationHandler("telegram", defaults=params)
    logger.addHandler(tg_handler)
    """Start the bot."""
    updater = Updater(telegram_api_token)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            QuizStates.CHOOSING: [
                RegexHandler('^Новый вопрос$', handle_new_question_request),
                RegexHandler('^Сдаться$', handle_give_up),
                MessageHandler(Filters.text, handle_solution_attempt),
            ]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
