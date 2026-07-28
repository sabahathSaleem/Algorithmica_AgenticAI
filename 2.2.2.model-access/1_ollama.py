from dotenv import load_dotenv, find_dotenv
from pydantic_ai import Agent
import os

# load .env from current directory or parents; most projects keep it at repo root
load_dotenv(find_dotenv())

# make sure the variable really exists (case matters on some OSes)
if not os.environ.get("OLLAMA_BASE_URL"):
    raise RuntimeError(
        "OLLAMA_BASE_URL is not set in the environment. "
        "Either add it to a .env file at the project root or set it manually, "
        "or instantiate the provider with OllamaProvider(base_url=...)"
    )

agent = Agent(
    'ollama:qwen3:4b',
    instructions="You are a helpful assistant.",
)

response = agent.run_sync("Write a haiku about recursion in programming.")
print(response.output)
print(response.usage())

response = agent.run_sync("What is recursion in programming.")
print(response.output)
print(response.usage())