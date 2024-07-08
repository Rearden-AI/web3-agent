import logging

from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from app.llm.utils import get_template 

from ..classes.chat_message_flow_state import ChatMessageFlowState
from ..constants import user_request_categories, glossary, supported_actions
from ...llm import get_model

logger = logging.getLogger('categorize_user_request')

model = get_model()

system_message_template = """
You are User Request Categorizer Agent You are master at understanding what a user wants to ask in chat and are able to categorize it in a useful way

SUPPORTED_ACTIONS_LIST
{{ supported_actions_list }}

{{ glossary }}

Conduct a comprehensive analysis of the user message provided and categorize into one of the following categories:
{{ catrgories_desctiptions }}
        
Output ONLY a single catgory only from the types: {{ category_list }} eg: off_topic 
"""

categorize_request_prompt = PromptTemplate(
    template=get_template(system_message_template),
    template_format="jinja2",
    input_variables=["user_message", "catrgories_desctiptions", "supported_actions_list", "glossary"]
)

catrgories_desctiptions = '\n'.join(map(lambda x: f"{x[0]} - {x[1]}", user_request_categories.items()))
category_list = ', '.join(map(lambda x: f'{x}', user_request_categories.keys()))
supported_actions_list = '\n'.join(supported_actions.values())

user_message_category_generator = (
    {
        "catrgories_desctiptions": lambda _: catrgories_desctiptions,
        "category_list": lambda _: category_list,
        "supported_actions_list": lambda _: supported_actions_list,
        "glossary": lambda _: glossary,
        "user_message": RunnablePassthrough()
    }
    | categorize_request_prompt
    | model
    | StrOutputParser()
)


async def categorize_user_request(state: ChatMessageFlowState):
    logger.info('Categorizing message')

    user_message = state['user_message']
    num_steps = int(state['num_steps'])
    num_steps += 1

    message_category = await user_message_category_generator.ainvoke(user_message)
    logger.info(message_category)

    return {'message_category': message_category, 'num_steps': num_steps}
