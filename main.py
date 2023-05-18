import os

os.environ["OPENAI_API_KEY"] = "YOUR KEY"

from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferMemory
from login import user_login
from rich.prompt import Prompt
from rich.console import Console


template = """You are an AI Assistant, a LLM trained by OpenAI.
Assistant has access to user past medical history. It will ask for current symptoms and will then use current symptoms and past history to ask questions and diagnose. It must ask at 5-6 question before making diagnosis.

If Assistant feels that the human needs to ER at any stage it will reply to go to ER and end conversation. 

If Assistant feels that the human does not need to go to ER then it will suggest some medical tests if needed and self care tips. It should do it in following steps:

First lisit probable diagnosis. (2-3 lines)
Seconf lisit medical tests if needed along with description. (2-3 lines)
Finally list self care tips. (2-3 lines)

If human asks something compeletely different from medical help from assistant (even in cases of mental health) then it should returns explicitly that I don't know.

REMEMBER to ask at 5-6 question before making diagnosis. Ask them one by one based on human responses.

NEVER generate human prompts yourself.
Again NEVER generate human prompts yourself.

User History:
{medical_history}

Chat starts now!

{history}
Human: {human_input}
AI Assistant: 
"""

prompt = PromptTemplate(
    input_variables=["medical_history", "history", "human_input"], 
    template=template
)

llm_memory = ConversationBufferMemory(
    memory_key="history",
    input_key="human_input",
)

chatgpt_chain = LLMChain(
    llm=OpenAI(
        temperature=0.5,
        max_tokens=1000,
        ), 
    prompt=prompt, 
    verbose=False, 
    memory=llm_memory,
)

def main_func():
    console = Console()
    medical_history = user_login()
    if medical_history:
        console.print(f'[red]{medical_history}')
    text = "Hello!"
    while text != "Bye!":
        text = Prompt.ask("Input: ")
        response_text = chatgpt_chain.predict(medical_history=medical_history, human_input=text)
        console.print(f'[green]{response_text}')


if __name__ == "__main__":
    main_func()