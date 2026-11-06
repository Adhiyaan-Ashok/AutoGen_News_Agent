
import asyncio
import os
from dotenv import load_dotenv

from ddgs import DDGS
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()


def search_the_internet(query: str) -> str:
    """Search the web and return useful results with URLs."""
    try:
        results = DDGS().text(query, max_results=8)

        if not results:
            return "No search results found."

        formatted_results = []

        for index, result in enumerate(results, start=1):
            formatted_results.append(
                f"""
                Result {index}
                Title: {result.get('title', '')}
                URL: {result.get('href', '')}
                Summary: {result.get('body', '')}
                """
            )

        return "\n".join(formatted_results)

    except Exception as error:
        return f"Web search error: {error}"


async def run_seo_agents(
    topic: str,
    audience: str = "General audience",
    location: str = "Global",
    content_type: str = "Blog article",
    word_count: int = 1200,
):
    """Execute four SEO agents sequentially."""

    model_client = OpenAIChatCompletionClient(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    # AGENT 1: RESEARCH AGENT
    research_agent = AssistantAgent(
        name="research_agent",
        model_client=model_client,
        tools=[search_the_internet],
        system_message="""
        You are an expert SEO Research Agent.

        Your responsibilities:
        1. Research the user's broad topic using web search.
        2. Identify promising specific subtopics and emerging trends.
        3. Identify primary and secondary SEO keywords.
        4. Explain search intent.
        5. Identify the target audience's questions and pain points.
        6. Provide supporting source URLs.
        7. Never invent statistics, sources, or search volume data.

        Present your findings in clear Markdown sections.
        """,
    )

    # AGENT 2: CONTENT WRITER
    writer_agent = AssistantAgent(
        name="content_writer_agent",
        model_client=model_client,
        system_message="""
        You are a professional SEO Content Writer.

        Write an original, engaging article using the research provided.

        Requirements:
        1. Follow the identified subtopic and search intent.
        2. Write for the specified target audience.
        3. Use a clear introduction and conclusion.
        4. Organize content using H1, H2 and H3 headings.
        5. Naturally include relevant keywords.
        6. Avoid keyword stuffing and unsupported claims.
        7. Follow the requested content type and word count.

        Return the complete article in Markdown.
        """,
    )

    # AGENT 3: SEO OPTIMIZER
    seo_agent = AssistantAgent(
        name="seo_optimizer_agent",
        model_client=model_client,
        system_message="""
        You are an expert Technical and On-Page SEO Optimizer.

        Improve the article without changing its factual meaning.

        Provide:
        1. SEO title.
        2. Meta description.
        3. Recommended URL slug.
        4. Primary and secondary keywords.
        5. Improved heading structure.
        6. Internal and external linking suggestions.
        7. Image alt-text suggestions.
        8. Readability and keyword placement improvements.

        Return the complete optimized article and SEO recommendations.
        """,
    )

    # AGENT 4: EDITORIAL REVIEWER
    reviewer_agent = AssistantAgent(
        name="editorial_reviewer_agent",
        model_client=model_client,
        system_message="""
        You are a senior Editorial Reviewer and SEO Quality Auditor.

        Review the optimized article for:
        1. Factual accuracy and unsupported claims.
        2. Grammar and spelling.
        3. Clarity and readability.
        4. Content structure and consistency.
        5. Search intent alignment.
        6. Keyword stuffing.
        7. SEO title and meta description quality.

        Correct identified problems.

        Do not invent facts or sources.
        Clearly flag claims that need independent verification.

        Return:
        A. Editorial review findings.
        B. Final corrected article.
        C. Final SEO recommendations.
        """,
    )

    try:
        # STEP 1: RESEARCH
        research_result = await research_agent.run(
            task=f"""
            Research this broad topic: {topic}

            Target audience: {audience}
            Target location: {location}
            Content type: {content_type}

            Identify the most promising specific subtopic.
            Include evidence and source URLs.
            """
        )

        research = str(research_result.messages[-1].content)

        # STEP 2: CONTENT WRITING
        writer_result = await writer_agent.run(
            task=f"""
            Write a {content_type} of approximately {word_count} words.

            Topic: {topic}
            Target audience: {audience}
            Target location: {location}

            Use this research:
            {research}
            """
        )

        draft = str(writer_result.messages[-1].content)

        # STEP 3: SEO OPTIMIZATION
        seo_result = await seo_agent.run(
            task=f"""
            Optimize this article for SEO.

            Research:
            {research}

            Original article:
            {draft}
            """
        )

        optimized = str(seo_result.messages[-1].content)

        # STEP 4: EDITORIAL REVIEW
        review_result = await reviewer_agent.run(
            task=f"""
            Perform the final editorial review.

            Research:
            {research}

            Optimized article:
            {optimized}
            """
        )

        final_review = str(review_result.messages[-1].content)

        return {
            "research": research,
            "draft": draft,
            "optimized": optimized,
            "final_review": final_review,
        }

    finally:
        await model_client.close()


def execute_seo_agents(
    topic,
    audience="General audience",
    location="Global",
    content_type="Blog article",
    word_count=1200,
):
    """Synchronous function for the Streamlit application."""

    return asyncio.run(
        run_seo_agents(
            topic=topic,
            audience=audience,
            location=location,
            content_type=content_type,
            word_count=word_count,
        )
    )
