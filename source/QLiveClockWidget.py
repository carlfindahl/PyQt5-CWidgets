import time
import copy
import datetime
import threading
from PyQt5 import QtCore
from PyQt5 import QtWidgets


class QLiveClockWidget(QtWidgets.QWidget):
    """The QLiveClockWidget is a widget which shows and updates
    a live system clock to display the time. It wraps a single
    QLabel, and runs the clock update in a separate thread.

    Signals:
    secondPassed -- Once every second
    newMinute -- Whenever there is a new minute
    newHour -- Whenever there is a new hour
    """
    secondPassed = QtCore.pyqtSignal()
    newMinute = QtCore.pyqtSignal(int)
    newHour = QtCore.pyqtSlot(int)

    def __init__(self, parent=None, align=0, precision=0.1):
        """Constructor for QLiveClockWidget

        Keyword Arguments:
        parent -- parent widget for this widget (default: None)
        align -- The clock text alignment (defualt: 0)
                 0 = Center
                 1 = Left
                 2 = Right
        precision -- The interval in seconds the clock should update (default: 0.1)

        Example:
        C = QLiveClockWidget()
        C.newMinute.connect(displayAlert)
        C.secondPassed.connect(updateAppData)
        C.newHour.connect(hourlyRoutine)
        """
        super().__init__(parent)
        self.__initUI()

        self.currentTime = datetime.datetime.now()

        self.__timeLock = threading.Lock()
        self.__updateThread = threading.Thread(target=self.__updateTime,
                                               args=[precision],
                                               daemon=True)
        self.__updateThread.start()

    def __initUI(self):
        """Initialize the UI"""

        # Setup widgets
        self._timeLabel = QtWidgets.QLabel(self)

        # Setup layouts
        self._hLayout = QtWidgets.QHBoxLayout()
        self._hLayout.addWidget(self._timeLabel)

        self.setLayout(self._hLayout)

        # Connect signals
        self.secondPassed.connect(self.__setLabelText)

    def __updateTime(self, precision):
        """Update the internal time and send relevant time change
        signals. Should be run in the internal clock thread.

        Arguments:
        precision -- The interval in seconds the clock should update
        """
        lastSecond = self.currentTime.second
        lastMinute = self.currentTime.minute
        lastHour = self.currentTime.hour

        while True:
            self.__timeLock.acquire()

            # New Second
            self.currentTime = datetime.datetime.now()
            if lastSecond < self.currentTime.second:
                self.secondPassed.emit()
                lastSecond = self.currentTime.second

            # New Minute
            if lastMinute < self.currentTime.minute:
                self.newMinute.emit(self.currentTime.minute)
                lastSecond = self.currentTime.second
                lastMinute = self.currentTime.minute

            # New Hour
            if lastHour < self.currentTime.hour:
                self.newHour.emit(self.currentTime.hour)
                lastSecond = self.currentTime.second
                lastMinute = self.currentTime.minute
                lastMinute = self.currentTime.hour

            self.__timeLock.release()

            time.sleep(precision)

    @QtCore.pyqtSlot()
    def __setLabelText(self):
        """Updates the text of the time label"""
        self.__timeLock.acquire()
        self._timeLabel.setText(self.currentTime.strftime("%H:%M:%S"))
        self.__timeLock.release()

    def getTime(self, asString=False):
        """Get the currently displayed time in datetime format

        Returns:
        datetime -- The current time as a datetime object
        string -- If the asString kwarg is set to True

        Keyword Arguments:
        asString -- Returns as string instead (default: False)

        Example:
        getTime(True) # returns for example "16:21:10"
        """
        if asString:
            return self.currentTime.strftime("%H:%M:%S")
        else:
            self.__timeLock.acquire()
            retVal = copy.copy(self.currentTime)
            self.__timeLock.release()
            return retVal
