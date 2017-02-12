from PyQt5 import QtWidgets


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
        self.__initUI()

    def __initUI(self):
        """Initialize the UI"""
        pass
