# help_window.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel

class HelpWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Help')
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()

        # 这里添加帮助信息
        help_text = (
            "这是帮助文档的内容。\n\n"
            "1. 该应用程序可以帮助用户做某些事情。\n"
            "2. 你可以点击菜单栏中的选项来使用不同的功能。\n"
            "3. 更多帮助内容请参考官网或文档。"
        )
        
        label = QLabel(help_text)
        layout.addWidget(label)
        self.setLayout(layout)
