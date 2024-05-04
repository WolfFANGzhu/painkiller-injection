class ControlPanel:
    def __init__(self):
        self._buttons = []

    def add_button(self, button):
        self._buttons.append(button)

    def remove_button(self, button):
        self._buttons.remove(button)

    def display(self):
        for button in self._buttons:
            button.display()