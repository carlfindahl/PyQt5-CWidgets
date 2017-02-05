from PyQt5 import QtWidgets

class QLabelledPromptWindow(QtWidgets.QDialog):
    def __init__(self, prompt: str, buttonText="Confirm"):
        """A basic Horizontally layed out prompt Window
        with a QLineEdit for accepting user input. Fetch
        the text using getInputText().

        Arguments:
        string prompt -- The prompt to provide the user

        Keyword Arguments
        string buttonText -- The text to show on the submit button
            Default: "Confirm"

        Example:
        QLabelledPromptWindow("State your name", "Confirm")
        """
        super(QLabelledPromptWindow, self).__init__()
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
