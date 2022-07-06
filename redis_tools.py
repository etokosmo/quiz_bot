import redis
from environs import Env

from get_questions_and_answers import get_quiz_bank


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

    quiz_db.flushall()

    for question, answer in get_quiz_bank().items():
        quiz_db.set(question, answer)


if __name__ == '__main__':
    main()
