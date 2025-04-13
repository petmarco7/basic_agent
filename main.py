from langchain_openai import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain.agents import Tool, create_tool_calling_agent, AgentExecutor, create_react_agent
from langchain_core.messages import SystemMessage, HumanMessage

from numpy import *

from writer import tools_writer
from explorer import tools_explorer
from reader import tools_reader

# Initialize the OpenAI LLM
llm = AzureChatOpenAI(
    model="ksb", 
    openai_api_key="219284af2cc5405ea9caf2278e3b1f81",
    azure_endpoint="https://mpe-test-ksb.openai.azure.com/",
    openai_api_version="2024-02-01",
    openai_api_type="azure",
    temperature=0
)

# Simple calculator tool function for Agent A
def calculator(expression: str) -> str:
    """A simple calculator tool: useful for mathematical calculations."""

    try:
        result = str(eval(expression))
    except Exception:
        result = "Unable to compute. Please provide a valid mathematical expression."
    return result

# Memory to store conversation history for both agents
memory_b = ConversationBufferMemory(memory_key="chat_history_agent_b", return_messages=True)

agent_b_tools = [
    Tool(name="population_france", func=lambda x: "67 million", description="outputs the population of France"),
    Tool(name="population_italy", func=lambda x: "63 million", description="outputs the population of Italy"),
    Tool(name="population_spain", func=lambda x: "47 million", description="outputs the population of Spain"),
]

prompt_agent_b = ChatPromptTemplate.from_messages(
    [
        ("system", """You are the expert of the world populations. You have access to the populations of France, Italy, and Spain, through the tools at your disposal.

                    You are part of a team, and you have to provide information to the team members.
         """),
        ("human", "Task: {input}"),
        ("placeholder", "{agent_scratchpad}"),
    ],
)

agent_q = create_tool_calling_agent(
    llm=llm, 
    tools=agent_b_tools, 
    prompt=prompt_agent_b,
)
agent_q_executor = AgentExecutor(agent=agent_q,
                                 tools=agent_b_tools,
                               memory=memory_b,
                               verbose=True)

# Chain for Agent B, where it provides further information
def ask_agent_b(input: str) -> str:
    """Ask Agent B for additional processing."""
    # Agent B uses the LLM to generate additional responses based on input
    # response_b = llm.invoke([
    #     SystemMessage("You are Agent B, a helpful assistant that provides additional information. The population of France is 67 million."),
    #     HumanMessage(input)
    # ])
    # return response_b.content

    response_b = agent_q_executor.invoke({"input": input})
    print(response_b)
    return response_b['output']

# Define tools for Agent A, including calculator and Agent B
tools = [
    Tool(name="calculator", func=calculator, description="A simple calculator tool for mathematical calculations."),
    Tool(name="agent_b", func=ask_agent_b, description="Agent B provides additional information processing."),
] + tools_writer + tools_explorer + tools_reader

# Define Agent A's prompt template
prompt_agent_a = ChatPromptTemplate.from_messages(
    [
        ("system", """You are the manager of a team. You have access to a set of tools that can help you accomplish tasks.
         In these tools, you also have access to an expert that can provide additional information.
         If you plan to use the expert, make sure to explain clearly the task to the expert.
                    
                    Before starting make a plan about how to accomplish the task. 
                    Reason about the steps you need to take and the tools you need to use: reason step by step.
         
                    Once the plan is ready, start executing it by using the tools at your disposal."""),
        ("human", "Task: {input}"),
        ("placeholder", "{agent_scratchpad}"),
    ],
)

# Create the structured chat agent for Agent A
agent_a = create_tool_calling_agent(
    llm=llm, 
    tools=tools, 
    prompt=prompt_agent_a,
)

memory_a = ConversationBufferMemory(memory_key="chat_history_agent_a", return_messages=True)

# Set up Agent Executor for Agent A
agent_executor = AgentExecutor(agent=agent_a,
                               tools=tools,
                               memory=memory_a,
                               verbose=True)

# Test query for Agent A
query = """I want you to create a folder 'build' in the current directory.
If the folder already exists, remove it and create a new one.

Write a .txt file 'example.txt' in the 'build' folder with the answer to the following question:
What is the sum of the population of France and Italy?
"""
response = agent_executor.invoke({"input": query})

print("Agent A response:")
print(response)