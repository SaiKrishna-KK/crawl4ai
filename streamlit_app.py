import asyncio
import streamlit as st
from crawl4ai.dependency_docs_manager import DependencyDocsManager

# Define dependencies and their docs URLs
DEPENDENCIES = {
    "playwright": "https://playwright.dev/python/docs/intro",
    "beautifulsoup4": "https://www.crummy.com/software/BeautifulSoup/bs4/doc/",
    "pydantic": "https://docs.pydantic.dev/latest/",
}

manager = DependencyDocsManager(DEPENDENCIES)

st.title("Documentation Search")

if st.button("Fetch Documentation"):
    asyncio.run(manager.fetch_docs())
    st.success("Documentation downloaded")

if st.button("Build Index"):
    asyncio.run(manager.llm_text.generate_index_files())
    st.success("Index built")

query = st.text_input("Search")
if st.button("Search") and query:
    result = manager.search(query, top_k=3)
    st.text(result)
