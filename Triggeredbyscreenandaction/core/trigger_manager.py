class TriggerManager:
    def __init__(self):
        self.triggers = []

    def add_trigger(self, trigger):
        self.triggers.append(trigger)

    def move_trigger(self, old_index, new_index):
        if 0 <= old_index < len(self.triggers) and 0 <= new_index < len(self.triggers):
            self.triggers.insert(new_index, self.triggers.pop(old_index))

    def check_triggers(self):
        for trigger in self.triggers:
            location = trigger.match()
            if location:
                trigger.execute_actions(location)
                break