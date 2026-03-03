from PyQt5.QtCore import QThread, pyqtSignal

class AIWorker(QThread): 
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, agent_executor, parser, input):
        super().__init__()
        self.agent_executor = agent_executor
        self.parser = parser
        self.input = input

    
    def run(self):
        try:
            agent_executor = self.agent_executor
            raw_response = agent_executor.invoke({"input": self.input})
            content = raw_response.get("output")
            structured_data = self.parser.parse(content)
  
            self.finished.emit(structured_data.dict()) 
        except Exception as e:
            self.error.emit(str(e))





