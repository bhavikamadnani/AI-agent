from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import tool
from datetime import datetime
from pydantic import BaseModel, Field

@tool
def search_tool(query: str):
    """Search the web for information using DuckDuckGo. 
    Use this for current events or facts you don't know."""
    search = DuckDuckGoSearchRun()
    return search.run(query)