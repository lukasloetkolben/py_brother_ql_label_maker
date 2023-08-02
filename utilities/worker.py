from PySide6.QtCore import QRunnable, QObject, Signal


class WorkerSignal(QObject):
    finished = Signal(object)


class Worker(QRunnable):

    def __init__(self, func, *args, **kwargs):
        super(WorkerSignal, self).__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

        self.signal = WorkerSignal()

    def run(self):
        result = self.func(*self.args, **self.kwargs)
        self.signal.finished.emit(result)
