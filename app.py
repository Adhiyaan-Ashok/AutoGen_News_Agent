
import streamlit as st
from agents import execute_seo_agents

st.set_page_config(
    page_title="AutoGen SEO Multi-Agent System",
    page_icon="🚀",
    layout="wide",
)

st.title("🚀 AutoGen SEO Multi-Agent System")
st.caption("AI-powered SEO research, content writing, optimization and editorial review")

st.sidebar.header("Content Settings")

audience = st.sidebar.text_input(
    "Target Audience",
    value="General audience",
)

location = st.sidebar.text_input(
    "Target Location",
    value="Global",
)

content_type = st.sidebar.selectbox(
    "Content Type",
    ["Blog article", "Website content", "Product review", "Tutorial"],
)

word_count = st.sidebar.number_input(
    "Target Word Count",
    min_value=300,
    max_value=5000,
    value=1200,
    step=100,
)

st.subheader("Enter Your SEO Topic")

topic = st.text_area(
    "What topic would you like the agents to research?",
    placeholder="Example: Artificial Intelligence in Healthcare",
    height=100,
)

if st.button("🚀 Start SEO Agent Workflow", type="primary"):
    if not topic.strip():
        st.warning("Please enter a topic.")
    else:
        try:
            with st.spinner(
                "Four AI agents are working sequentially. Please wait..."
            ):
                results = execute_seo_agents(
                    topic=topic,
                    audience=audience,
                    location=location,
                    content_type=content_type,
                    word_count=int(word_count),
                )

            st.success("All four agents completed successfully!")

            tab1, tab2, tab3, tab4 = st.tabs(
                [
                    "🔎 Research",
                    "✍️ Content Draft",
                    "📈 SEO Optimization",
                    "✅ Final Review",
                ]
            )

            with tab1:
                st.markdown("### Research Agent Results")
                st.markdown(results["research"])

            with tab2:
                st.markdown("### Content Writer Results")
                st.markdown(results["draft"])

            with tab3:
                st.markdown("### SEO Optimizer Results")
                st.markdown(results["optimized"])

            with tab4:
                st.markdown("### Editorial Reviewer Results")
                st.markdown(results["final_review"])

            st.divider()
            st.subheader("Download Agent Outputs")

            for key, filename in [
                ("research", "research.md"),
                ("draft", "content_draft.md"),
                ("optimized", "seo_optimized.md"),
                ("final_review", "final_article.md"),
            ]:
                st.download_button(
                    label=f"Download {filename}",
                    data=results[key],
                    file_name=filename,
                    mime="text/markdown",
                    key=f"download_{key}",
                )

        except Exception as error:
            st.error(f"Workflow failed: {error}")
            st.exception(error)

st.divider()
st.caption("Powered by Microsoft AutoGen, OpenAI and DuckDuckGo Search")
