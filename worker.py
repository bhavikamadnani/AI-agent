from PyQt5.QtCore import QThread, pyqtSignal
from langchain_core.prompts import ChatPromptTemplate


class AIWorker(QThread): 
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, agent_executor, parser, input, prompt):
        super().__init__()
        self.agent_executor = agent_executor
        self.parser = parser
        self.input = input
        self.prompt = prompt
    def run(self, prompt):
        try:
            chain = prompt | self.agent_executor | self.parser 
            raw_response = chain.invoke({"input": self.input})
            content = raw_response.get("output", "")
            structured_data = self.parser.parse(content)
  
            self.finished.emit(structured_data.dict()) 
        except Exception as e:
            self.error.emit(str(e))


