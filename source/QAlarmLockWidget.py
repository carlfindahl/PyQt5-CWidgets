import time
import threading
from PyQt5 import QtCore
from PyQt5 import QtWidgets


class QAlarmLockWidget(QtWidgets.QWidget):
    """The QAlarmLockWidget is a widget that pops up on your screen
    and (potentially) soft-locks it for a given amount of time with
    a custom message. Useful for making alarm applications that
    need to remind you to do certain tasks at, or away from the
    computer. Hence why it can soft-lock your workstation for a given
    amount of time.
    """

    alarmUnlocked = QtCore.pyqtSignal()

    def __init__(self, parent=None, message="Alarm", locks=False, lockTime=5):
        """Constructor for QAlarmLockWidget

        Keyword Arguments:
        parent -- parent widget for this widget (default: None)
        message (str) -- The message to display when opening the Alarm!
        locks -- true if alarm should lock the screen (default: False)
        lockTime (int) -- seconds screen should be locked. Only relevant
                          when locks = True. (default: 60)

        Example:
        A = QAlarmLockWidget(locks=True, lockTime=10.0)
        A.alarmUnlocked.connect(A.close) # Auto Close
        """
        super().__init__(parent)
        self.__initUI(message, locks)

        if locks:
            self.unlockTime = time.time() + int(lockTime)
            self.unlockThread = threading.Thread(target=self.__checkForUnlock)
            self.unlockThread.start()

    def __initUI(self, message, isLocked):
        """Initializes the UI

        Arguments:
        message -- The message passed from the constructor. Used to
                   initialize the alarm message.
        isLocked -- Used to make the close button locked or unlocked
                    by default
        """

        # Make it fullscreen
        size = QtWidgets.QApplication.desktop().screenGeometry()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setGeometry(0, 0, size.width(), size.height())

        self.setStyleSheet("background-color: #FF0000;")

        # Setup widgets
        self._alarmMessage = QtWidgets.QLabel(self)
        self._alarmMessage.setStyleSheet("font-size: 72px;")
        self._alarmMessage.setText(message)

        self._closeButton = QtWidgets.QPushButton("CLOSE")
        if self.locked:
            self._closeButton.setEnabled(False)
        self._closeButton.clicked.connect(self.close)
        self._closeButton.setStyleSheet("background-color: #FFF; font-size: 20px;")

        # Setup layouts
        self._hLayout = QtWidgets.QHBoxLayout()
        self._hLayout.addStretch()
        self._hLayout.addWidget(self._alarmMessage)
        self._hLayout.addStretch()

        self._vLayout = QtWidgets.QVBoxLayout()
        self._vLayout.addLayout(self._hLayout)
        self._vLayout.addWidget(self._closeButton)

        self.setLayout(self._vLayout)

    def __checkForUnlock(self):
        """A check run by the unlock thread if the widget should be locked.
        Will update the close button text, and re-enable it after the given
        unlock time. Don't call manually.
        """
        while time.time() < self.unlockTime:
            self._closeButton.setText(f"UNLOCK IN {self.unlockTime - time.time():0.0f}s...")
            time.sleep(1)
        self._closeButton.setText("CLOSE")
        self._closeButton.setEnabled(True)
        self.alarmUnlocked.emit()
