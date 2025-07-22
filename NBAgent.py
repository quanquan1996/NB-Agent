from strands import Agent, tool
from strands_tools import calculator, current_time
from strands import Agent
from strands.models import BedrockModel
import asyncio
# Define a custom tool as a Python function using the @tool decorator
@tool
def letter_counter(word: str, letter: str) -> int:
    """
    Count occurrences of a specific letter in a word.

    Args:
        word (str): The input word to search in
        letter (str): The specific letter to count

    Returns:
        int: The number of occurrences of the letter in the word
    """
    if not isinstance(word, str) or not isinstance(letter, str):
        return 0

    if len(letter) != 1:
        raise ValueError("The 'letter' parameter must be a single character")

    return word.lower().count(letter.lower())

# Create an agent with tools from the strands-tools example tools package
# as well as our custom letter_counter tool
bedrock_model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    region_name="us-west-2",
    temperature=0.3,
)
nb_agent = Agent(model=bedrock_model,tools=[calculator, current_time, letter_counter])
# # Ask the agent a question that uses the available tools
# message = """
# I have 4 requests:
#
# 1. What is the time right now?
# 2. Calculate 3111696 / 74088
# 3. Tell me how many letter R's are in the word "strawberry" 🍓
# 4. Output a script that does what we just spoke about!
#    Use your python tools to confirm that the script works before outputting it
# """
# async def process_streaming_response():
#     agent_stream = nb_agent.stream_async(message)
#     async for event in agent_stream:
#         print(event)
# asyncio.run(process_streaming_response())