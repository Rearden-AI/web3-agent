from .llama_3_constants import *

default_user_message_template = """
USER_MESSAGE:
{{ user_message }}
"""


def get_prefix_template(system_message: str):
    return f"{BEGIN_OF_TEXT}{SYSTEM_MESSAGE_START}{system_message}{END_OF_MESSAGE}"


def get_suffix_template():
    return f"{USER_MESSAGE_START}{default_user_message_template}{END_OF_MESSAGE}{ASSISTANT_MESSAGE_START}"


def get_few_shot_template():
    assistant_message = "{{ assistant_message }}"
    return f"{USER_MESSAGE_START}{default_user_message_template}{END_OF_MESSAGE}{ASSISTANT_MESSAGE_START}{assistant_message}{END_OF_MESSAGE}"


def get_template(system_message: str, user_message: str=default_user_message_template):
    return f"{get_prefix_template(system_message=system_message)}{USER_MESSAGE_START}{user_message}{END_OF_MESSAGE}{ASSISTANT_MESSAGE_START}"


def get_template_for_few_shot(system_message: str, user_message: str, assistant_message: str):
    return f"{get_template(system_message=system_message, user_message=user_message)}{assistant_message}"
