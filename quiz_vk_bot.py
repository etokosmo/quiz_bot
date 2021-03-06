import logging

import vk_api as vk
from environs import Env
from notifiers.logging import NotificationHandler
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from format_answer import format_answer
from redis_tools import auth_redis

logger = logging.getLogger(__name__)


def handle_new_question_request(event, vk_api, keyboard, quiz_db):
    question = quiz_db.randomkey()
    quiz_db.set(event.user_id, question)
    vk_api.messages.send(
        peer_id=event.user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message=question
    )


def handle_solution_attempt(event, vk_api, keyboard, quiz_db):
    question = quiz_db.get(event.user_id)
    answer = format_answer(quiz_db.get(question))
    user_answer = format_answer(event.text)
    if (user_answer in answer) and (len(answer) * 0.25 < len(user_answer)):
        vk_api.messages.send(
            peer_id=event.user_id,
            random_id=get_random_id(),
            keyboard=keyboard.get_keyboard(),
            message="""Правильно! Поздравляю!
            Для следующего вопроса нажми «Новый вопрос»
            """
        )
    else:
        vk_api.messages.send(
            peer_id=event.user_id,
            random_id=get_random_id(),
            keyboard=keyboard.get_keyboard(),
            message="Неправильно… Попробуешь ещё раз?"
        )


def handle_give_up(event, vk_api, keyboard, quiz_db):
    question = quiz_db.get(event.user_id)
    answer = quiz_db.get(question)
    vk_api.messages.send(
        peer_id=event.user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message=f"Правильный ответ: {answer}"
    )


def create_keyboard():
    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)

    keyboard.add_line()
    keyboard.add_button('Мой счет', color=VkKeyboardColor.POSITIVE)
    return keyboard


def main():
    logging.basicConfig(
        format='%(asctime)s : %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S',
        level=logging.INFO
    )

    env = Env()
    env.read_env()
    vk_api_token = env("VK_API_TOKEN")
    telegram_api_token = env("TELEGRAM_API_TOKEN")
    telegram_chat_id = env("TELEGRAM_CHAT_ID")
    redis_address = env("REDIS_ADDRESS")
    redis_port = env("REDIS_PORT")
    redis_password = env("REDIS_PASSWORD")

    quiz_db = auth_redis(redis_address, redis_port, redis_password)

    params = {
        'token': telegram_api_token,
        'chat_id': telegram_chat_id
    }
    tg_handler = NotificationHandler("telegram", defaults=params)
    logger.addHandler(tg_handler)

    vk_session = vk.VkApi(token=vk_api_token)
    vk_api = vk_session.get_api()

    keyboard = create_keyboard()

    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        try:
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text == "Сдаться":
                    handle_give_up(event, vk_api, keyboard, quiz_db)
                if event.text == "Новый вопрос":
                    handle_new_question_request(event, vk_api, keyboard,
                                                quiz_db)
                else:
                    handle_solution_attempt(event, vk_api, keyboard, quiz_db)
        except Exception as err:
            logging.error("Error was raising:", err)


if __name__ == "__main__":
    main()
