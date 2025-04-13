from langchain_openai import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain.agents import Tool, create_tool_calling_agent, AgentExecutor

from numpy import *

from writer import tools_writer
from explorer import tools_explorer
from reader import tools_reader

llm = AzureChatOpenAI(
    model="ksb", 
    openai_api_key="219284af2cc5405ea9caf2278e3b1f81",
    azure_endpoint="https://mpe-test-ksb.openai.azure.com/",
    openai_api_version="2024-02-01",
    openai_api_type="azure",
    temperature=0
)

# memory = ConversationBufferMemory(memory_key="backend_buffer", return_messages=True)

tools = [
    tools_writer + tools_explorer + tools_reader
]

prompt_backend_developer = ChatPromptTemplate.from_messages(
    [
        ("system","""You are an experienced backend developer.
                    Your goal is to write backend code to create a server for a web application.
                      
                      Make sure to use the tools at your disposal to provide the best possible answers to the user's questions.

                      Before starting, make a plan about how to accomplish the task at hand.
                      Reason about the steps you need and the tools you can use to achieve the desired outcome.

                      Once you have a plan, start implementing it by using the tools you have available.
         
                    End the conversation by finishing with <SUCCCESS> or <FAILURE> to indicate the outcome of the task.
                      """),
        ("user", "Task: {input}"),
        ("placeholder", "{agent_scratchpad}")
    ]
)
backend_dev = create_tool_calling_agent(
        llm=llm,
        tools=tools,
        prompt=prompt_backend_developer,
    )

backend_developer = AgentExecutor(
        agent=backend_dev,
    tools=tools,
    # memory=memory,
    verbose=True
    )

def ask_backend_developer(input: str) -> str:
    response = backend_developer.invoke({"input": input})
    return response.content