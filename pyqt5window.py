from PyQt5.QtWidgets import QWidget     
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from worker import AIWorker

class ResearchModel(QWidget):
    def __init__(self, executor, parser):
        super().__init__()
        self.entry_label = QLabel("What can I help you with?", self)
        self.query_input = QLineEdit(self)
        self.enter_button = QPushButton("Enter", self)
        self.topic_label = QLabel(self)
        self.summary_label = QLabel(self)
        self.sources_label = QLabel(self)
        self.tools_used_label = QLabel(self)
        self.executor = executor
        self .parser = parser
        self.initUI()

    def initUI(self) :
        self.setWindowTitle("Research Ai Agent")
        
        vbox = QVBoxLayout()

        vbox.addWidget(self.entry_label)
        vbox.addWidget(self.query_input)
        vbox.addWidget(self.enter_button)
        vbox.addWidget(self.topic_label)
        vbox.addWidget(self.summary_label)
        vbox.addWidget(self.sources_label)
        vbox.addWidget(self.tools_used_label)

        self.setLayout(vbox)
        self.entry_label.setWordWrap(True)
        self.topic_label.setWordWrap(True)
        self.summary_label.setWordWrap(True)
        self.sources_label.setWordWrap(True)
        self.tools_used_label.setWordWrap(True)
        self.show()

        self.entry_label.setAlignment(Qt.AlignCenter)
        self.query_input.setAlignment(Qt.AlignCenter)
        self.topic_label.setAlignment(Qt.AlignCenter)
        self.summary_label.setAlignment(Qt.AlignCenter)
        self.sources_label.setAlignment(Qt.AlignCenter)
        self.tools_used_label.setAlignment(Qt.AlignCenter)

        self.entry_label.setObjectName("entry_label")
        self.query_input.setObjectName("query_input")
        self.enter_button.setObjectName("enter_button")
        self.topic_label.setObjectName("topic_label")
        self.summary_label.setObjectName("summary_label")
        self.sources_label.setObjectName("sources_label")
        self.tools_used_label.setObjectName("tools_used_label")

        self.setStyleSheet("""
                                QLabel, QPushButton{
                           font-family: calibri;
                           } 
                           QLabel#entry_label{
                           font-size: 40px;
                           font-style: italic;
                           }
            QLineEdit#query_input{
                           font-size: 35px;
                           }
            QPushButton#enter_button{
                           font-size: 35px;
                           font-weight: bold;
                           } 
            QLabel#topic_label{
                           font-size: 45px;
                           }  
            QLabel#summary_label{
                           font-size: 40px;
                           font-family: calibri;
                           }
            QLabel#sources_label{
                           font-size: 35px;
                           }
            Qlabel#tools_used_label{
                           font-size: 35px;
                           }
            """)
        
        self.enter_button.clicked.connect(self.start_research)
    
 
    def start_research(self) :
        input = self.query_input.text()
        if not input:
            return

        self.enter_button.setEnabled(False) 
        self.entry_label.setText("Researching... please wait.")

        self.worker = AIWorker(self.executor, self.parser, prompt= input)
        self.worker.finished.connect(self.handle_success)
        self.worker.error.connect(self.handle_error)
        self.worker.start()
    
    def handle_success(self, data):
        self.topic_label.setText(data['topic'])
        self.summary_label.setText(data['summary'])
        self.sources_label.setText(", ".join(data['sources']))
        self.enter_button.setEnabled(True)
        self.entry_label.setText("Research Done.")

    def handle_error(self, err_msg):
        self.entry_label.setText(f"AI ERROR: {err_msg}")
        self.enter_button.setEnabled(True)
   
    