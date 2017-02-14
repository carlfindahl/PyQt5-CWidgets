import sys, subprocess
import Resources
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from QConsoleOutputWidget import QConsoleOutputWidget


class QConsoleInputWidget(QtWidgets.QWidget):
    """The QConsoleInputWidget allows you to send console input
    to a running subprocess.Popen() object through stdin.
    """

    def __init__(self, process, parent=None):
        """Constructor for QConsoleInputWidget

        Arguments:
        process -- process to send stdin to

        Keyword Arguments:
        parent -- parent widget for this widget (default: None)

        Example:
        QConsoleInputWidget()
        """
        super().__init__(parent)
        QtGui.QFontDatabase().addApplicationFont(Resources.monspaceFont)
        self.__initUI()
        self.process = process

    def __initUI(self):
        """Initialize the UI"""
        self.setWindowTitle("Console Input")

        self._inputField = QtWidgets.QLineEdit(self)
        self._inputField.setFont(QtGui.QFont("Ubuntu Mono"))
        self._submitButton = QtWidgets.QPushButton("Submit", self)

        self._layout = QtWidgets.QHBoxLayout()
        self._layout.addWidget(self._inputField)
        self._layout.addWidget(self._submitButton)

        self.setLayout(self._layout)

        with open(Resources.consoleStyle, "r") as CSS:
            self._inputField.setStyleSheet(CSS.read())

        self._submitButton.clicked.connect(self.sendInputToProcess)

    def clearInputData(self):
        """Clear the input field, wiping all text from it"""
        self._inputField.clear()

    def getInputData(self):
        """Get the current input in the inputField

        Returns:
        string -- The text in the input field

        Example:
        x = getInputData()
        """
        return self._inputField.text()

    def send(self, data):
        """Send data to the stdin of the attached process

        Arguments:
        data -- The data to send through stdin
        """
        try:
            self.process.stdin.write(data.encode())
        except:
            self.process.stdin.write(data)

    def sendInputToProcess(self):
        """Gets the input text, clears the field, and then sends the
        data to the attached process.
        """
        data = self.getInputData()
        self.clearInputData()
        self.send(data)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    p = subprocess.Popen(["python"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)

    output = QConsoleOutputWidget()
    output.addProcess(p)
    output.show()

    inputt = QConsoleInputWidget(p)
    inputt.show()

    sys.exit(app.exec_())
