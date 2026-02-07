from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel, set_tracing_disabled
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# Disable tracing to avoid 401 errors if no OpenAI Key is present
set_tracing_disabled(True)

# Initialize the OpenAI client for Gemini
gemini_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Define the Gemini model configuration
GEMINI_MODEL = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash-lite",
    openai_client=gemini_client
)