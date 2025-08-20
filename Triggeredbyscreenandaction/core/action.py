import pyautogui

class Action:
    def __init__(self, action_type, direction=None, repeat=1):
        self.action_type = action_type
        self.direction = direction
        self.repeat = repeat

    def execute(self, location):
        if not location:
            return

        x, y = location
        if self.action_type == "Click":
            pyautogui.click(x, y)
            print(f"{location}을 클릭")
        elif self.action_type == "Drag":
            pyautogui.moveTo(x, y)
            print(f"{location}. Details need implementation.")
        elif self.action_type == "Scroll":
            pyautogui.moveTo(x, y)
            print(f"Scroll performed at {location}. Details need implementation.")