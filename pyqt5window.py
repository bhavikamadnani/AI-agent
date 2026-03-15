# I refactored your entire ui file lol 
# things look better now so thank me later
# PyQt5 imports
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QListWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from worker import AIWorker


class ResearchModel(QWidget):
    """Modern Research Agent UI.

    - Input at top with an action button
    - Topic displayed as a large header
    - Summary shown in a wrapped, read-only QTextEdit
    - Sources and tools shown in list widgets
    - Status label for progress/errors
    """

    def __init__(self, executor, parser):
        super().__init__()
        self.executor = executor
        self.parser = parser

        # Widgets
        self.header = QLabel("Research AI Agent")
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setObjectName("header")

        self.entry_label = QLabel("What can I help you with?")
        self.entry_label.setAlignment(Qt.AlignCenter)
        self.entry_label.setObjectName("entry_label")

        # Explicit labels for UI divisions
        self.input_label = QLabel("Input")
        self.input_label.setAlignment(Qt.AlignLeft)
        self.input_label.setObjectName("input_label")

        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Enter a research question, e.g. 'Effects of microplastics on marine life'")
        self.query_input.setObjectName("query_input")

        self.enter_button = QPushButton("Search")
        self.enter_button.setObjectName("enter_button")

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setObjectName("status_label")

        self.topic_label = QLabel("")
        self.topic_label.setAlignment(Qt.AlignCenter)
        self.topic_label.setObjectName("topic_label")

        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.setLineWrapMode(QTextEdit.WidgetWidth)
        self.summary_text.setObjectName("summary_text")

        self.summary_label = QLabel("Summary")
        self.summary_label.setAlignment(Qt.AlignLeft)
        self.summary_label.setObjectName("summary_label")

        self.sources_list = QListWidget()
        self.sources_list.setObjectName("sources_list")

        self.tools_list = QListWidget()
        self.tools_list.setObjectName("tools_list")

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Research AI")
        self.setMinimumSize(900, 600)

        # Layouts
        main = QVBoxLayout()
        main.setSpacing(12)
        main.setContentsMargins(18, 18, 18, 18)

        main.addWidget(self.header)
        main.addWidget(self.entry_label)

        # Input row with explicit label above
        main.addWidget(self.input_label)
        input_row = QHBoxLayout()
        input_row.addWidget(self.query_input)
        input_row.addWidget(self.enter_button)
        main.addLayout(input_row)

        main.addWidget(self.status_label)
        main.addWidget(self.topic_label)

        # Content area split: summary on top, sources/tools below
        main.addWidget(self.summary_label)
        main.addWidget(self.summary_text, stretch=3)

        bottom_row = QHBoxLayout()

        # Left column: Sources (with label)
        left_col = QVBoxLayout()
        self.sources_label = QLabel("Sources")
        self.sources_label.setAlignment(Qt.AlignLeft)
        self.sources_label.setObjectName("sources_label")
        left_col.addWidget(self.sources_label)
        left_col.addWidget(self.sources_list)

        # Right column: Tools used (with label)
        right_col = QVBoxLayout()
        self.tools_label = QLabel("Tools Used")
        self.tools_label.setAlignment(Qt.AlignLeft)
        self.tools_label.setObjectName("tools_label")
        right_col.addWidget(self.tools_label)
        right_col.addWidget(self.tools_list)

        bottom_row.addLayout(left_col, stretch=1)
        bottom_row.addLayout(right_col, stretch=1)
        main.addLayout(bottom_row)

        self.setLayout(main)

        # Simple, modern styling
        self.setStyleSheet(
            """
            QWidget{
                background: #f5f7fa;
                font-family: 'Segoe UI', Roboto, Arial;
                color: #222;
            }
            QLabel#header{
                font-size: 24px;
                font-weight: 700;
                color: #0b3d91;
                margin-bottom: 6px;
            }
            QLabel#entry_label{
                font-size: 14px;
                color: #444;
            }
            QLineEdit#query_input{
                padding: 10px;
                font-size: 14px;
                border-radius: 8px;
                border: 1px solid #ccd6e6;
                background: white;
            }
            QPushButton#enter_button{
                padding: 10px 18px;
                font-size: 14px;
                border-radius: 8px;
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #4e8ef7, stop:1 #2f6fe6);
                color: white;
                border: none;
                min-width: 120px;
            }
            QTextEdit#summary_text{
                background: white;
                border-radius: 10px;
                padding: 12px;
                border: 1px solid #e0e6ef;
                font-size: 15px;
            }
            QListWidget#sources_list, QListWidget#tools_list{
                background: white;
                border-radius: 8px;
                padding: 8px;
                border: 1px solid #e0e6ef;
                font-size: 13px;
            }
            QLabel#status_label{
                font-size: 13px;
                color: #666;
            }
            QLabel#topic_label{
                font-size: 20px;
                font-weight: 600;
                color: #223;
                margin-top: 8px;
                margin-bottom: 8px;
            }
            """
        )

        # Connect
        self.enter_button.clicked.connect(self.start_research)

    def start_research(self):
        query = self.query_input.text().strip()
        if not query:
            return

        # Clear old results
        self.topic_label.setText("")
        self.summary_text.clear()
        self.sources_list.clear()
        self.tools_list.clear()

        self.enter_button.setEnabled(False)
        self.status_label.setText("Researching... please wait.")

        # start worker thread
        self.worker = AIWorker(self.executor, self.parser, query)
        self.worker.finished.connect(self.handle_success)
        self.worker.error.connect(self.handle_error)
        self.worker.start()

    def handle_success(self, data):
        # Defensive access to returned dict
        topic = data.get("topic") or "(no topic)"
        summary = data.get("summary") or ""
        sources = data.get("sources") or []
        tools_used = data.get("tools_used") or []

        self.topic_label.setText(topic)
        self.summary_text.setPlainText(summary)

        self.sources_list.clear()
        for s in sources:
            self.sources_list.addItem(str(s))

        self.tools_list.clear()
        for t in tools_used:
            self.tools_list.addItem(str(t))

        self.enter_button.setEnabled(True)
        self.status_label.setText("Research Done.")

    def handle_error(self, err_msg):
        self.status_label.setText(f"AI ERROR: {err_msg}")
        self.enter_button.setEnabled(True)
   

    
