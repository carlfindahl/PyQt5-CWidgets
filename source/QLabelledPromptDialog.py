from PyQt5 import QtWidgets

class QLabelledPromptDialog(QtWidgets.QDialog):
    """A window that unconditionally asks for user input, and
    that does not care if it receives any, or if it is considered
    valid. It will simply prompt and receive. Any validation will
    have to be done later.
    """

    def __init__(self, prompt, buttonText="Confirm"):
        """Constructor for QLabelledPromptDialog

        Arguments:
        string prompt -- The prompt to provide the user

        Keyword Arguments
        string buttonText -- The text to show on the submit button
            Default: "Confirm"

        Example:
        QLabelledPromptDialog("State your name", "Confirm")
        """

        super().__init__()
        self.setGeometry(800, 400, 600, 50)
        self.setWindowTitle(prompt)

        self._titleLabel = QtWidgets.QLabel(self)
        self._titleLabel.setText(prompt)

        self._inputField = QtWidgets.QLineEdit(self)

        self._confirmButton = QtWidgets.QPushButton(self)
        self._confirmButton.setText(buttonText)
        self._confirmButton.clicked.connect(self.__confirmClicked)

        __layout = QtWidgets.QVBoxLayout(self)
        __layout.addStretch() # Ensure label stays with the input field
        __layout.addWidget(self._titleLabel)
        __layout.addWidget(self._inputField)
        __layout.addWidget(self._confirmButton)

        self.setLayout(__layout)

    def empty(self):
        """Returns True if the input text field is empty."""
        return len(self._inputField.text()) == 0

    def getInputText(self):
        """Return the string value currently in self._inputField"""
        return self._inputField.text()

    def __confirmClicked(self):
        """Will close the window"""
        self.accept()
