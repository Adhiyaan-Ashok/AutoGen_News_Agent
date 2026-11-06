
import os
import asyncio
from dotenv import load_dotenv
from ddgs import DDGS

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient


# STEP 1: Create the DuckDuckGo search tool
def search_weather_news(city: str) -> str:
    """
    Search the web for current weather information
    and latest weather-related news for a given city.

    Args:
        city: Name of the city.

    Returns:
        Weather search results with source URLs.
    """

    try:
        results = DDGS().text(
            f"current weather and latest weather news in {city}",
            max_results=5
        )

        if not results:
            return f"No weather information found for {city}."

        output = []

        for item in results:
            output.append(
                f"Title: {item.get('title', '')}\n"
                f"Information: {item.get('body', '')}\n"
                f"Source: {item.get('href', '')}"
            )

        return "\n\n".join(output)

    except Exception as e:
        return f"Weather search failed: {str(e)}"


# STEP 2: Create the AutoGen agent
async def main():

    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file")

    model_client = OpenAIChatCompletionClient(
        model=os.getenv("OPENAI_MODEL") or "gpt-4o-mini",
        api_key=api_key
    )

    weather_agent = AssistantAgent(
        name="weather_news_agent",
        model_client=model_client,
        tools=[search_weather_news],

        system_message="""
        You are a Weather News Assistant.

        Always use search_weather_news to retrieve information.

        Never invent weather conditions or news.

        Return exactly 3 short lines:
        Line 1: Current weather.
        Line 2: Forecast or latest weather news.
        Line 3: Source URL.
        """,

        reflect_on_tool_use=True
    )

    city = input("\nEnter city name: ").strip()

    if not city:
        print("Please enter a valid city.")
        await model_client.close()
        return

    print("\nSearching weather information...\n")

    try:
        result = await weather_agent.run(
            task=f"Find current weather and latest weather news for {city}."
        )

        print("\n========== WEATHER NEWS ==========\n")
        print(result.messages[-1].content)

    finally:
        await model_client.close()


# STEP 3: Run the application
if __name__ == "__main__":
    asyncio.run(main())
