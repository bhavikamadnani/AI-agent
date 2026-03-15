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

            # various possible output shapes into a single string
            if isinstance(content, str):
                content_str = content
            elif isinstance(content, list):
                parts = []
                for item in content:
                    if isinstance(item, str):
                        parts.append(item)
                    elif isinstance(item, dict):
                        # common keys that may contain the LLM text
                        text = item.get("text") or item.get("content") or item.get("message")
                        if isinstance(text, str):
                            parts.append(text)
                        else:
                            parts.append(str(item))
                    else:
                        parts.append(str(item))
                content_str = "\n".join(parts)
            elif isinstance(content, dict):
                content_str = content.get("text") or content.get("content") or str(content)
            else:
                content_str = str(content)

            structured_data = self.parser.parse(content_str)

            self.finished.emit(structured_data.dict())
        except Exception as e:
            self.error.emit(str(e))





