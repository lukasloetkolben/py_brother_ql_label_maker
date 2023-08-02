from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap, QPalette, QImage, QResizeEvent, QTransform
from PySide6.QtWidgets import QWidget, QGridLayout, QSizePolicy, QLabel


class PreviewComponent(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Widgets
        self.pixmap = QPixmap()
        self.image_label = QLabel()
        self.image_label.setBackgroundRole(QPalette.Base)
        self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        # Layout
        self.layout = QGridLayout()
        self.layout.addWidget(QLabel("Preview"), 1, 0, Qt.AlignTop)

        self.layout.addWidget(self.image_label, 1, 0, Qt.AlignCenter)
        self.setLayout(self.layout)

    def show_image(self, file_path: Path, rotation=0):
        """
        Show the image from the provided file_path in the PreviewComponent.
        """
        image = QImage(file_path)

        if rotation != 0:
            transform = QTransform().rotate(rotation)
            image = image.transformed(transform)

        self.pixmap = QPixmap.fromImage(image)
        self.image_label.setPixmap(self.pixmap)
        self.resizeEvent(None)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """
        Override the default resizeEvent to resize the displayed image accordingly.
        """
        if event is not None:
            super(PreviewComponent, self).resizeEvent(event)
        if not self.pixmap.isNull():
            scaled_pixmap = self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
