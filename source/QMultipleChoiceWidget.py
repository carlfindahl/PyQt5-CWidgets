from PyQt5 import QtWidgets

class QMultipleChoiceWidget(QtWidgets.QWidget):
    """A dynamically populated widget with buttons that link
    to functions. Great if you need to provide the user with
    multiple choices that are unique to each other.
    """

    def __init__(self, buttonDictionary, parent=None):
        """Constructor for QMultipleChoiceWidget

        Arguments:
        dict(buttonText, buttonFunction) buttonDictionary -- Dictionary
            with buttons that should be spawned in this widget.

        Keyword Arguments:
        QWidget parent -- Widget to be the parent of this widget

        Exceptions:
        The constructor will raise a logic error if the buttonDictionary
        is empty.

        Example:
        QMultipleChoiceWidget({"Option 1" : someFunction,
                               "Option 2" : someOtherfunction})
        """

        super().__init__(parent)

        if len(buttonDictionary) == 0:
            raise  Exception("The buttonDictionary argument can not be empty")

        self.setGeometry(800, 400, 300, 80)
        self.setWindowTitle("Select an Option")

        self.Buttons = {}
        self.__layout = QtWidgets.QGridLayout()

        for k, v in buttonDictionary.items():
            self.Buttons[k] = QtWidgets.QPushButton(self)
            self.Buttons[k].setText(k)
            self.Buttons[k].clicked.connect(v)
            self.Buttons[k].clicked.connect(lambda: self.close())
            self.__layout.addWidget(self.Buttons[k])

        self.setLayout(self.__layout)
