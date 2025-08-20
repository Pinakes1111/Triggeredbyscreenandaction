import sys
import win32gui
import keyboard
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QLabel, QHBoxLayout, QComboBox

from gui.trigger_panel import TriggerPanel
from gui.action_panel import ActionPanel
from gui.roi_selector import ROISelector
from core.trigger_manager import TriggerManager
from core.window_monitor import WindowMonitor
from core.trigger import Trigger
from core.action import Action

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("화면에 반응하는 매크로")
        self.resize(950, 600)

        self.layout = QVBoxLayout(self)

        window_selection_layout = QHBoxLayout()
        window_selection_layout.addWidget(QLabel("목표 윈도우:"))
        self.window_list_combo = QComboBox()
        window_selection_layout.addWidget(self.window_list_combo)
        self.refresh_button = QPushButton("새로고침")
        self.refresh_button.clicked.connect(self.refresh_window_list)
        window_selection_layout.addWidget(self.refresh_button)
        self.layout.addLayout(window_selection_layout)

        self.refresh_window_list()

        self.trigger_list_widget = QListWidget()
        self.layout.addWidget(QLabel("트리거"))
        self.layout.addWidget(self.trigger_list_widget)

        self.trigger_panel = TriggerPanel()
        self.action_panel = ActionPanel()
        self.layout.addWidget(self.trigger_panel)
        self.layout.addWidget(self.action_panel)

        btn_layout = QHBoxLayout()
        self.add_trigger_button = QPushButton("트리거 추가")
        self.start_button = QPushButton("모니터링 시작")
        self.stop_button = QPushButton("모니터링 중지")
        self.move_up_button = QPushButton("위로")
        self.move_down_button = QPushButton("아래로")
        self.select_roi_button = QPushButton("감지 영역 선택")

        btn_layout.addWidget(self.add_trigger_button)
        btn_layout.addWidget(self.start_button)
        btn_layout.addWidget(self.stop_button)
        btn_layout.addWidget(self.move_up_button)
        btn_layout.addWidget(self.move_down_button)
        btn_layout.addWidget(self.select_roi_button)
        self.layout.addLayout(btn_layout)

        self.add_trigger_button.clicked.connect(self.add_trigger_to_list)
        self.start_button.clicked.connect(self.start_monitoring)
        self.stop_button.clicked.connect(self.stop_monitoring)
        self.move_up_button.clicked.connect(self.move_trigger_up)
        self.move_down_button.clicked.connect(self.move_trigger_down)
        self.select_roi_button.clicked.connect(self.select_roi)

        self.trigger_manager = TriggerManager()
        self.monitor = WindowMonitor(self.trigger_manager)

        self.roi_selector = ROISelector()
        self.roi_selector.roiSelected.connect(self.on_roi_selected)

        keyboard.add_hotkey('esc', self.stop_monitoring)

    def refresh_window_list(self):
        self.window_list_combo.clear()
        self.windows = {}

        def enum_windows_proc(hwnd, lParam):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                title = win32gui.GetWindowText(hwnd)
                self.windows[title] = hwnd
                self.window_list_combo.addItem(title)
            return True

        win32gui.EnumWindows(enum_windows_proc, None)

    def select_roi(self):
        selected_title = self.window_list_combo.currentText()
        if not selected_title:
            print("먼저 대상 창을 선택해주세요.")
            return

        hwnd = self.windows.get(selected_title)
        if hwnd and win32gui.IsWindow(hwnd):
            rect = win32gui.GetWindowRect(hwnd)
            target_qrect = QRect(rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1])
            self.roi_selector.start_selection(target_qrect)
        else:
            print("선택한 창 핸들이 더 이상 유효하지 않습니다. 목록을 새로고침 해주세요.")
            self.refresh_window_list()

    def on_roi_selected(self, roi):
        print(f"ROI 선택됨: {roi.x()}, {roi.y()}, {roi.width()}, {roi.height()}")
        self.trigger_panel.set_roi(roi)

    def add_trigger_to_list(self):
        trigger = self.trigger_panel.create_trigger()
        action = self.action_panel.create_action()
        if trigger and action:
            trigger.add_action(action)
            self.trigger_manager.add_trigger(trigger)

            template_filename = trigger.template_path.split('/')[-1]
            action_display_text = self.action_panel.action_combo.currentText()
            item_text = f"ROI: ({trigger.roi.x()},{trigger.roi.y()}), 템플릿: {template_filename}, 액션: {action_display_text}"
            self.trigger_list_widget.addItem(item_text)

    def move_trigger_up(self):
        current_row = self.trigger_list_widget.currentRow()
        if current_row > 0:
            item = self.trigger_list_widget.takeItem(current_row)
            self.trigger_list_widget.insertItem(current_row - 1, item)
            self.trigger_manager.move_trigger(current_row, current_row - 1)
            self.trigger_list_widget.setCurrentRow(current_row - 1)

    def move_trigger_down(self):
        current_row = self.trigger_list_widget.currentRow()
        if current_row < self.trigger_list_widget.count() - 1:
            item = self.trigger_list_widget.takeItem(current_row)
            self.trigger_list_widget.insertItem(current_row + 1, item)
            self.trigger_manager.move_trigger(current_row, current_row + 1)
            self.trigger_list_widget.setCurrentRow(current_row + 1)

    def start_monitoring(self):
        if not self.monitor.is_alive():
            self.monitor = WindowMonitor(self.trigger_manager)
            self.monitor.start()
            print("모니터링을 시작했습니다.")

    def stop_monitoring(self):
        if self.monitor.is_alive():
            self.monitor.stop()
            print("모니터링을 중지했습니다.")