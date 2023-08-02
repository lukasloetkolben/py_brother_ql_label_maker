from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLabel


class Icon(QLabel):

    def __init__(self, icon: QIcon, size: int = 14):
        super(Icon, self).__init__()
        self.setPixmap(icon.pixmap(QSize(size, size)))
