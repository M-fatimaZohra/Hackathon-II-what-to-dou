from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel, set_tracing_disabled
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# Disable tracing to avoid 401 tracing errors if no OpenAI Key is present
set_tracing_disabled(True)

groq_client = AsyncOpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# Use this object in the 'model' field of Agent()
GROQ_MODEL = OpenAIChatCompletionsModel(
    model="llama-3.3-70b-versatile",
    openai_client=groq_client
)