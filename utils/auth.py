import os

from dotenv import load_dotenv

os.environ.clear()
load_dotenv()


def connection_str():
    return os.getenv('CONNECTION_STR')


def namespace_name():
    return os.getenv('FULLY_QUALIFIED_NAMESPACE')


def topic_name():
    return os.getenv('TOPIC_NAME')


def subscription_name():
    return os.getenv('SUBSCRIPTION_NAME')
