##########################################################################
# PyPipe - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
Module that defines a QT line edit widget associated with a timer in order to
signal user modification only after an inactivity period.
"""

# Third party import
from PySide2 import QtCore, QtWidgets


class QLineEditModificationTimer(QtCore.QObject):

    '''
    A QLineEditModificationTimer instance is accociated to a
    QtWidgets.QLineEdit instance, it listens all user modification (Qt
    signal 'textChanged( const QString & )') and emits a
    signal 'userModification()' when timerInterval milliseconds passed
    since the last user modification.
    '''
    # Default timer interval in milliseconds
    defaultTimerInterval = 2000
    userModification = QtCore.Signal()

    def __init__(self, qLineEdit, timerInterval=None):
        '''
        Parameters
        ----------
        qLineEdit: (QtWidgets.QLineEdit instance)
            widget associated with this QLineEditModificationTimer.
        timerInterval: (milliseconds)
            minimum inactivity period before emitting
            userModification signal. Default value is
            QLineEditModificationTimer.defaultTimerInterval

        see: TimeredQLineEdit
        '''

        QtCore.QObject.__init__(self)
        # QLineEdit<qt.QLineEdit> instance associated with this
        # QLineEditModificationTimer
        self.qLineEdit = qLineEdit
        if timerInterval is None:
            self.timerInterval = self.defaultTimerInterval
        else:
            # minimum inactivity period before emitting C{userModification}
            # signal.
            self.timerInterval = timerInterval
        self.__timer = QtCore.QTimer(self)
        self.__timer.setSingleShot(True)
        self.__internalModification = False
        self.qLineEdit.textChanged.connect(self._userModification)
        # self.qLineEdit.lostFocus.connect(self._noMoreUserModification)
        self.qLineEdit.editingFinished.connect(self._noMoreUserModification)
        self.__timer.timeout.connect(self.modificationTimeout)

    def close(self):
        self.stop()
        self.qLineEdit.textChanged.disconnect(self._userModification)
        # self.qLineEdit.lostFocus.disconnect(self._noMoreUserModification)
        self.qLineEdit.editingFinished.disconnect(self._noMoreUserModification)
        self.__timer.timeout.disconnect(self.modificationTimeout)

    def _userModification(self, value):
        if not self.__internalModification:
            self.__timer.start(self.timerInterval)

    def modificationTimeout(self):
        self.userModification.emit()  # self.qLineEdit.text())

    def _noMoreUserModification(self):
        if self.__timer.isActive():
            self.__timer.stop()
            self.userModification.emit()  # self.qLineEdit.text())

    def stopInternalModification(self):
        '''
        Stop emitting C{userModification} signal when associated
        L{QLineEdit<qt.QLineEdit>} is modified.

        @see: L{startInternalModification}
        '''
        self.__internalModification = False

    def startInternalModification(self):
        '''
        Restart emitting C{userModification} signal when associated
        L{QLineEdit<qt.QLineEdit>} is modified.

        @see: L{stopInternalModification}
        '''
        self.__internalModification = True

    def stop(self):
        '''
        Stop the timer if it is active.
        '''
        self.__timer.stop()

    def isActive(self):
        '''
        Returns True if the timer is active, or False otherwise.
        '''
        return self.__timer.isActive()


#-------------------------------------------------------------------------
class TimeredQLineEdit(QtWidgets.QLineEdit):

    '''
    Create a L{QLineEdit<QtWidgets.QLineEdit>} instance that has an private attribute
    containing a L{QLineEditModificationTimer} associated to C{self}. Whenever
    the internal L{QLineEditModificationTimer} emits a C{SIGNAL(
    'userModification' )} signal, this signal is also emited by the
    L{TimeredQLineEdit} instance.
    '''

    userModification = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        '''
        All non keyword parameters of the constructor are passed to
        L{QLineEdit<QtWidgets.QLineEdit>} constructor. An optional C{timerInterval}
        keyword parameter can be given, it is passed to
        L{QLineEditModificationTimer} constructor. At the time this class was
        created, L{QLineEdit<qt.QLineEdit>} constructor did not accept keyword
        parameters.
        '''
        timerInterval = kwargs.pop('timerInterval', None)
        if kwargs:
            QtWidgets.QLineEdit.__init__(self, *args, **kwargs)
        else:
            QtWidgets.QLineEdit.__init__(self, *args)
        self.__timer = QLineEditModificationTimer(self,
                                                  timerInterval=timerInterval)
        self.__timer.userModification.connect(self.userModification)

    def stopInternalModification(self):
        '''
        @see: L{QLineEditModificationTimer.stopInternalModification}
        '''
        self.__timer.stopInternalModification()

    def startInternalModification(self):
        '''
        @see: L{QLineEditModificationTimer.startInternalModification}
        '''
        self.__timer.startInternalModification()

    def close(self):
        self.__timer.close()
        super(TimeredQLineEdit, self).close()
