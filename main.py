#main imports
from dotenv import load_dotenv
from pydantic import BaseModel
from PyQt5.QtWidgets import QApplication
import sys 
import warnings
warnings.filterwarnings("ignore", message= "Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater.")
from langchain_core.output_parsers import PydanticOutputParser, CommaSeparatedListOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_google_genai import ChatGoogleGenerativeAI 
from google import genai
from tools import search_tool
from pyqt5window import ResearchModel

#AI agent, response management and instructions
load_dotenv()
client = genai.Client(api_key="GEMINI_API_KEY")

class ResearchResponse(BaseModel) : 
        topic: str
        summary: str
        sources: list[str]
        tools_used: list[str]
        
def setup_agent():
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")                     
    parser = PydanticOutputParser(pydantic_object= ResearchResponse)

    prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
             You are a research assistant that will help generate a research paper.
             Answer the user query and use necessary tools.
             Wrap the output in this format and provide no other text\n{format_instructions}
             """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
        ).partial(format_instructions=parser.get_format_instructions())
                
    tools = [search_tool]

    agent = create_tool_calling_agent(
    llm=llm.bind_tools(tools),
    tools=tools,
    prompt= prompt
)
    return AgentExecutor(agent= agent, tools= tools, verbose= False), parser 

#show window
if __name__ == "__main__":
    print("Step 1: Starting App...")
    app = QApplication(sys.argv)
    
    print("Step 2: Setting up Agent (this might take a second)...")
    executor, parser = setup_agent()
    
    print("Step 3: Creating Window...")
    window = ResearchModel(executor, parser)
    
    print("Step 4: Showing Window...")
    window.show()
    
    print("Step 5: Entering Main Loop...")
    sys.exit(app.exec_())
 



        
    
