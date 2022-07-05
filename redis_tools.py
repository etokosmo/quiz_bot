import redis
from environs import Env

from get_questions_and_answers import get_quiz_bank


def fill_db_questions(quiz_bank_db):
    for question, answer in get_quiz_bank().items():
        quiz_bank_db.set(question, answer)


def set_user_question(quiz_bank_db, user_id, question):
    quiz_bank_db.set(user_id, question)


def get_user_question(quiz_bank_db, user_id):
    question = quiz_bank_db.get(user_id)
    return question


def get_random_question(quiz_bank_db):
    return quiz_bank_db.randomkey()


def get_answer(quiz_bank_db, question):
    answer = quiz_bank_db.get(question)
    return answer


def delete_all(quiz_bank_db):
    quiz_bank_db.flushall()


def auth_redis(redis_address, redis_port, redis_password):
    redis_obj = redis.Redis(host=redis_address, port=redis_port,
                            password=redis_password,
                            charset="utf-8",
                            decode_responses=True)
    return redis_obj


def main():
    env = Env()
    env.read_env()
    redis_address = env("REDIS_ADDRESS")
    redis_port = env("REDIS_PORT")
    redis_password = env("REDIS_PASSWORD")
    quiz_db = auth_redis(redis_address, redis_port, redis_password)
    delete_all(quiz_db)
    fill_db_questions(quiz_db)


if __name__ == '__main__':
    main()
