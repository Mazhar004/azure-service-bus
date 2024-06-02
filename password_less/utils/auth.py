from dotenv import load_dotenv
import os

load_dotenv()


def namespace_name():
    return os.getenv('FULLY_QUALIFIED_NAMESPACE')


def topic_name():
    return os.getenv('TOPIC_NAME')


def subscription_name():
    return os.getenv('SUBSCRIPTION_NAME')
