import sys
import threading
import subprocess
import Resources
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets


class QConsoleOutputWidget(QtWidgets.QWidget):
    """The QConsoleOutputWidget handles redirection of
    stdout / stderr, by showing it in a QtWidget instead
    of your regular console. It is designed for
    subprocess.Popen objects.
    """
    readStdout = QtCore.pyqtSignal(str)

    def __init__(self, parent=None, title="Console Output"):
        """Constructor for QConsoleOutputWidget.

        Keyword Arguments:
        parent -- parent widget for this widget (default: None)
        title -- Title for the window (default: "Console Output")

        Example:
        QConsoleOutputWidget()
        QConsoleOutputWidget(title="Program Output")
        """
        super().__init__(parent)
        self.setWindowTitle(str(title))
        self.setGeometry(800, 400, 600, 200)

        QtGui.QFontDatabase().addApplicationFont(Resources.monspaceFont)

        self.messageQueue = []
        self.__processes = []
        self.__processThreads = []
        self.__printLock = threading.Lock()

        self.__initUI()

    def __initUI(self):
        """Initialize the UI"""
        self.__layout = QtWidgets.QVBoxLayout()

        self.__console = QtWidgets.QTextEdit(self)
        self.__console.setFont(QtGui.QFont("Ubuntu Mono"))
        self.__console.setMinimumWidth(400)
        self.__console.setMinimumHeight(100)
        self.__console.setReadOnly(True)

        self.__layout.addWidget(self.__console)
        self.setLayout(self.__layout)

        with open(Resources.consoleStyle, "r") as CSS:
            self.__console.setStyleSheet(CSS.read())

        # Connect Signals
        self.__console.textChanged.connect(self.__scrollOnTextChanged)
        self.readStdout.connect(self.printToConsole)

    def __scrollOnTextChanged(self):
        """This method scrolls down to the bottom of the console when
        new text is added to it.
        """
        pass

    def __readFromProcess(self, process):
        """Method used internally by threads to read from a process
        until it has ended. Before returning, the thread will clean
        up the process, ensuring it is terminated and closed

        Arguments:
        process -- The process to track in this thread
        """
        while True:
            print("Reading")
            output = process.stdout.readline()
            print("Read done")
            if output == '' and process.poll() is not None:
                break
            if output:
                self.readStdout.emit(output.strip())

    def addProcess(self, process):
        """Adds a process to show output for to the console window.
        The added process should be made with: stdout=subprocess.PIPE
        stderr=subprocess.STDOUT and universal_newlines=True in order
        to work properly.

        Arguments:
        process -- The subprocess.Popen process to start tracking

        Exceptions:
        ValueError -- If the process is not of type subprocess.Popen

        Example:
        addProcess(Popen(["python"], stdout=PIPE))
        """
        if (not isinstance(process, subprocess.Popen)):
            raise ValueError("process must be a subprocess.Popen object")

        self.__processes.append(process)
        newThread = threading.Thread(target=self.__readFromProcess, args=(process,))
        newThread.daemon = True
        newThread.start()
        self.__processThreads.append(newThread)

    @QtCore.pyqtSlot(str)
    def printToConsole(self, message):
        """Prints the message to the console. Ensures that no
        other thread will attempt to print at the same time.

        Arguments:
        message -- String to print to the Console

        Example:
        printToConsole("I promise to be good!")
        """
        self.__printLock.acquire()
        self.__console.append(message)
        self.__printLock.release()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    console = QConsoleOutputWidget()
    console.show()
    p = subprocess.Popen(["python", "testScript.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    console.addProcess(p)
    sys.exit(app.exec_())
