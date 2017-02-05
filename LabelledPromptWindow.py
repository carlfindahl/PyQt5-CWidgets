from PyQt5 import QtWidgets

class LabelledPromptWindow(QtWidgets.QDialog):
    def __init__(self, Prompt: str, ButtonText="Confirm"):
        """A basic Horizontally layed out Prompt Window
        with a QLineEdit for accepting user input.

        Arguments:
        string Prompt -- The prompt to provide the user

        Keyword Arguments
        string ButtonText -- The text to show on the submit button
            Default: "Confirm"

        Example:
        LabelledPromptWindow("State your name", "Confirm")
        """
        super().__init__()
        self.setGeometry(800, 400, 600, 50)
        self.setWindowTitle(Prompt)

        # PROTECTED
        self._titleLabel = QtWidgets.QLabel(self)
        self._titleLabel.setText(Prompt)

        self._inputField = QtWidgets.QLineEdit(self)

        self._confirmButton = QtWidgets.QPushButton(self)
        self._confirmButton.setText(ButtonText)
        self._confirmButton.clicked.connect(self.confirmClicked)

        # PRIVATE
        __layout = QtWidgets.QVBoxLayout(self)
        __layout.addStretch() # Ensure label stays with the input field
        __layout.addWidget(self._titleLabel)
        __layout.addWidget(self._inputField)
        __layout.addWidget(self._confirmButton)

        self.setLayout(__layout)

    def confirmClicked(self):
        """Will close the window"""
        self.accept()

    def getInputText(self):
        """Return the string value currently in self._inputField"""
        return self._inputField.text()
