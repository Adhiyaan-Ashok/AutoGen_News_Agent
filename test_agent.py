import asyncio
import os

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()


async def main():

    # Configure OpenAI LLM
    model_client = OpenAIChatCompletionClient(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    # Create first AutoGen agent
    assistant = AssistantAgent(
        name="seo_assistant",
        model_client=model_client,
        system_message="You are an expert SEO assistant. Answer clearly and professionally."
    )

    # Send a task to the agent
    result = await assistant.run(
        task="Explain SEO in five simple points."
    )

    # Display agent response
    print("\n========== AUTOGEN AGENT RESPONSE ==========\n")
    print(result.messages[-1].content)

    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())