import cv2
import numpy as np
import pyautogui

class Trigger:
    def __init__(self, roi, template_path, threshold=0.8):
        self.roi = roi
        self.template_path = template_path

        try:
            stream = open(template_path, "rb")
            bytes_data = bytearray(stream.read())
            numpy_array = np.asarray(bytes_data, dtype=np.uint8)
            self.template = cv2.imdecode(numpy_array, cv2.IMREAD_GRAYSCALE)
        except Exception as e:
            print(f"Error loading template image: {e}")
            self.template = None

        if self.template is None:
            raise FileNotFoundError(f"Template image not found or failed to load at {template_path}")

        self.threshold = threshold
        self.actions = []

    def add_action(self, action):
        self.actions.append(action)

    def match(self):
        try:
            screenshot = pyautogui.screenshot(region=(self.roi.x(), self.roi.y(), self.roi.width(), self.roi.height()))
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

            res = cv2.matchTemplate(frame, self.template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)

            if max_val >= self.threshold:
                match_abs_x = self.roi.x() + max_loc[0]
                match_abs_y = self.roi.y() + max_loc[1]

                template_h, template_w = self.template.shape
                center_x = match_abs_x + template_w // 2
                center_y = match_abs_y + template_h // 2

                return (center_x, center_y)
        except Exception as e:
            print(f"Error during matching: {e}")

        return None

    def execute_actions(self, location):
        for action in self.actions:
            action.execute(location)