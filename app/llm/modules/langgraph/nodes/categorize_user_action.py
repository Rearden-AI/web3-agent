import logging

from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from app.llm.utils import get_few_shot_template, get_prefix_template, get_suffix_template 

from ..classes.chat_message_flow_state import ChatMessageFlowState
from ..constants import glossary, supported_actions
from ...llm import get_model

logger = logging.getLogger('categorize_user_action')

model = get_model()

supported_actions_descriptions = '\n'.join(map(lambda x: f"{x[0]} - {x[1]}", supported_actions.items()))
supported_actions_list = ', '.join(map(lambda x: f'{x}', supported_actions.keys()))

system_message_template = """
You are User Request Categorizer Agent You are master at understanding what action wants to perform and are able to categorize it in a useful way

{{ glossary }}

Conduct a comprehensive analysis of the user message provided and categorize needed action into one of the following categories:
{{ supported_actions_descriptions }}

You can ONLY output a single catgory only from types: {{ supported_actions_list }}
eg: transfer
"""

prefix = get_prefix_template(system_message=system_message_template)

few_shot_template = FewShotPromptTemplate(
    prefix=prefix,
    template_format="jinja2",
    example_prompt=PromptTemplate(
        template=get_few_shot_template(),
        input_variables=["user_message", "assistant_message"],
        template_format="jinja2"
    ),
    examples=
    [
        {
            "user_message": "I would like to get some yield on my eth",
            "assistant_message": "invest"
        },
        {
            "user_message": "I would like to send my usdt to another wallet",
            "assistant_message": "transfer"
        },
        {
            "user_message": "i want to send 10 ETH",
            "assistant_message": "transfer"
        },
        {
            "user_message": "I want to buy some usdt",
            "assistant_message": "swap"
        },
    ],
    suffix=get_suffix_template(),
    input_variables=["supported_actions_descriptions", "supported_actions_list", "glossary", "user_message"]
)

user_action_category_generator = (
    {
        "supported_actions_descriptions": lambda _: supported_actions_descriptions,
        "supported_actions_list": lambda _: supported_actions_list,
        "glossary": lambda _: glossary,
        "user_message": RunnablePassthrough()
    }
    | few_shot_template
    | model
    | StrOutputParser()
)


def categorize_user_action(state: ChatMessageFlowState):
    logger.info('Catogorizing action')

    user_message = state['user_message']
    num_steps = int(state['num_steps'])
    num_steps += 1

    action_category = user_action_category_generator.invoke(user_message)
    logger.info(action_category)

    return {"action_category": action_category, 'num_steps': num_steps}