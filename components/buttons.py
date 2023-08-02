from PySide6.QtGui import QIcon, QMovie
from PySide6.QtWidgets import QPushButton
from config import COLORS

class BaseButton(QPushButton):

    def __init__(self, *args, **kwargs):
        super(BaseButton, self).__init__(*args, **kwargs)
        self.setFixedHeight(25)
        self._movie = None

    def set_movie(self, movie: QMovie):
        self._movie = movie
        self._movie.frameChanged.connect(self.update_movie)
        self._movie.start()
        self.setIcon(QIcon(self._movie.currentPixmap()))

    def update_movie(self):
        self.setIcon(QIcon(self._movie.currentPixmap()))

    def stop_movie(self):
        if self._movie:
            self._movie.frameChanged.disconnect(self.update_movie)
            self._movie.stop()

    def remove_icon(self):
        self.stop_movie()
        self.setIcon(QIcon())


class PrimaryButton(BaseButton):
    def __init__(self, *args, **kwargs):
        super(PrimaryButton, self).__init__(*args, **kwargs)
        self.setStyleSheet(f"background-color:{COLORS.get(' primary-800')}; color:white;")


class SecondaryButton(BaseButton):
    def __init__(self, *args, **kwargs):
        super(SecondaryButton, self).__init__(*args, **kwargs)
        self.setStyleSheet(f"background-color:{COLORS.get('bluegray-400')}; color:white;")


class DangerButton(BaseButton):
    def __init__(self, *args, **kwargs):
        super(DangerButton, self).__init__(*args, **kwargs)
        self.setStyleSheet(f"background-color:{COLORS.get('red-700')}; color:white;")


class TransparentButton(BaseButton):
    def __init__(self, *args, **kwargs):
        super(TransparentButton, self).__init__(*args, **kwargs)
        self.setStyleSheet(f"background-color:rgba(0,0,0,0); color:black;")
