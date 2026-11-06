# AutoGen SEO Multi-Agent System

A small Streamlit application that turns a topic into researched, SEO-oriented content. Four Microsoft AutoGen agents work in sequence, using OpenAI for language generation and DuckDuckGo search for web research.

## What it does

1. Accepts a topic, target audience, location, content type, and approximate word count.
2. Researches the topic and identifies a focused subtopic, keywords, search intent, audience questions, and source URLs.
3. Writes a draft based on the research.
4. Optimizes the draft for on-page SEO, including metadata and content recommendations.
5. Reviews and edits the optimized content, flagging claims that may need verification.
6. Displays each stage in Streamlit tabs and offers the outputs as Markdown downloads.

## Agent and tool concepts

- **Agent:** An AutoGen `AssistantAgent` uses a model client and role-specific instructions to complete a task.
- **Model client:** `OpenAIChatCompletionClient` connects the agents to the configured OpenAI model.
- **Tool use:** The research agent calls `search_the_internet`, which retrieves DuckDuckGo results and returns titles, summaries, and URLs.
- **Sequential workflow:** Each agent's result is passed as input to the next agent: research → writing → SEO optimization → editorial review.
- **Frontend:** Streamlit collects settings, runs the workflow, and presents and downloads the results.
- **Async execution:** The workflow uses `async` AutoGen calls; `execute_seo_agents` provides a synchronous wrapper for the Streamlit app.

## Project files

- `app.py` — Streamlit interface and workflow presentation.
- `agents.py` — Search tool and the four-agent SEO workflow.
- `test_agent.py` — Minimal standalone AutoGen assistant example.
- `weather_news_agent.py` — Standalone weather and news search agent.
- `requirements.txt` — Dependencies for the main application and examples.
- `requirement1.txt` — Additional dependency notes.

## Requirements

- Python
- An OpenAI API key
- Internet access for the OpenAI API and DuckDuckGo search

## Setup

From the project directory, create and activate a virtual environment in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a `.env` file in the project directory:

```dotenv
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
```

`OPENAI_MODEL` is optional; the application defaults to `gpt-4o-mini`. Keep `.env` private and do not commit real API keys.

## Run the SEO application

```powershell
streamlit run app.py
```

Open the local URL printed by Streamlit, enter a topic, adjust the settings if needed, and select **Start SEO Agent Workflow**.

## Run the standalone examples

```powershell
python test_agent.py
python weather_news_agent.py
```

The weather example asks for a city and returns current weather-related search results. It also requires `OPENAI_API_KEY`.

## Notes

- Search results and generated content depend on external services and may be incomplete or inaccurate. Verify important claims and cited sources before publication.
- The target word count is an instruction to the writing agent, not a guaranteed exact length.
- `test_agent.py` is an example script; it does not define an automated test suite.
