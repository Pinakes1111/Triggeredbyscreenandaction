from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QFileDialog, QVBoxLayout, QHBoxLayout
from core.trigger import Trigger

class TriggerPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("트리거 설정"))

        h_layout = QHBoxLayout()
        self.template_label = QLabel("템플릿 이미지:")
        self.template_path_line = QLineEdit()
        self.template_button = QPushButton("이미지 선택")
        h_layout.addWidget(self.template_label)
        h_layout.addWidget(self.template_path_line)
        h_layout.addWidget(self.template_button)
        layout.addLayout(h_layout)

        self.roi_label = QLabel("감시 영역(ROI)이 설정되지 않았습니다.")
        layout.addWidget(self.roi_label)

        self.template_button.clicked.connect(self.select_template)

        self.roi = None
        self.template_path = None

    def select_template(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "템플릿 이미지 선택", "", "이미지 파일 (*.png *.jpg *.bmp)")
        if file_path:
            self.template_path_line.setText(file_path)
            self.template_path = file_path

    def set_roi(self, roi):
        self.roi = roi
        self.roi_label.setText(f"감시 영역(ROI) 설정됨: ({roi.x()}, {roi.y()}) - {roi.width()}x{roi.height()}")

    def create_trigger(self):
        if self.roi and self.template_path:
            try:
                return Trigger(self.roi, self.template_path)
            except FileNotFoundError as e:
                print(e)
                return None
        print("감시할 영역(ROI)이나 템플릿 이미지가 선택되지 않았습니다.")
        return None
    #트리거에 패스를 전달