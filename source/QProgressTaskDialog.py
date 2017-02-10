from PyQt5 import QtWidgets


class QProgressTaskDialog(QtWidgets.QDialog):
    """A widget which shows a progress bar and tracks
    a task that can be cancelled by the user.
    """

    def __init__(self, taskName):
        """Constructor for QProgressTaskDialog

        Arguments:
        string taskName -- Title of the window and label before progress bar

        Example:
        W = QProgressTaskDialog("Clearing Forest")
        for i in range(100):
            if not W.isCancelled():
                W.setProgress(i + 1)
            else:
                W.close()
        """

        super().__init__()

        self.setGeometry(800, 400, 600, 70)
        self.setWindowTitle(taskName)

        self.__taskLabel = QtWidgets.QLabel(self)
        self.__taskLabel.setText(taskName)

        self.__subTaskLabel = QtWidgets.QLabel(self)
        self.__subTaskLabel.setText("Working...")

        self.__progressBar = QtWidgets.QProgressBar(self)

        self.__cancelButton = QtWidgets.QPushButton(self)
        self.__cancelButton.clicked.connect(self.__cancelTask)
        self.__cancelButton.setText("Cancel")

        __hLayout = QtWidgets.QHBoxLayout()
        __hLayout.addWidget(self.__taskLabel)
        __hLayout.addWidget(self.__progressBar)
        __hLayout.addWidget(self.__cancelButton)

        __vLayout = QtWidgets.QVBoxLayout(self)
        __vLayout.addLayout(__hLayout)
        __vLayout.addWidget(self.__subTaskLabel)
        __vLayout.addStretch()

        self.setLayout(__vLayout)

        self.__cancelled = False
        self.__progress = 0
        self.__maxProgress = 100

    def setProgress(self, value):
        """Set the progress of the task as a number between 0 and 100

        Arguments:
        int value -- The new progress value (0 - 100)

        Example:
        for i in xrange(200):
            W.setProgress(i / 200 * 100)
        """
        if value > 100:
            value = 100
        elif value < 0:
            value = 0
        self.__progressBar.setValue(value)

    def setProgressWithCancel(self, value):
        """Does the same as setProgress, except will raise an exception if
        you attempt to call it after the user has requested to cancel the
        operation."""
        if self.isCancelled():
            raise Exception("The progress could not be set, as the user has requested to cancel!")
        else:
            self.setProgress(value)

    def getProgress(self):
        """Returns the current Progress value as a number between 0 and 100"""
        return self.__progress

    def isCancelled(self):
        """Returns true if the user has requested to Cancel the task."""
        return self.__cancelled

    def __cancelTask(self):
        """Requests the task to be cancelled. Up to the programmer to respect the wish"""
        self.__cancelled = True
