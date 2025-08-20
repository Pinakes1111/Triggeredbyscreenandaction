from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout
from core.action import Action

class ActionPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.action_map = {
            "클릭": "Click",
            "드래그": "Drag",
            "스크롤": "Scroll"
        }

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("액션 설정"))

        h_layout = QHBoxLayout()
        self.action_label = QLabel("액션 종류:")
        self.action_combo = QComboBox()
        self.action_combo.addItems(self.action_map.keys())
        h_layout.addWidget(self.action_label)
        h_layout.addWidget(self.action_combo)
        layout.addLayout(h_layout)

    def create_action(self):
        display_text = self.action_combo.currentText()
        if display_text:
            action_type = self.action_map.get(display_text)
            if action_type:
                return Action(action_type)
        return None