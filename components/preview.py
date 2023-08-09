import shutil
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QPalette, QImage, QResizeEvent, QTransform
from PySide6.QtWidgets import QWidget, QLabel, QFileDialog, QVBoxLayout

import components
from components.buttons import SuccessButton
from utilities.settings import Settings


class PreviewComponent(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_path = None

        # Widgets
        self.pixmap = QPixmap()
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter);
        self.image_label.setBackgroundRole(QPalette.Base)
        self.save_as_button = SuccessButton("Save as...", clicked=self.save_as_clicked)
        self.save_as_button.setEnabled(False)

        # Layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignVCenter)
        self.layout.addWidget(QLabel("Preview"))
        self.layout.addStretch()
        self.layout.addWidget(self.save_as_button)
        self.setLayout(self.layout)

    def show_image(self, file_path: Path, rotation=0):
        """
        Show the image from the provided file_path in the PreviewComponent.
        """
        self.file_path = file_path
        image = QImage(file_path)

        if rotation != 0:
            transform = QTransform().rotate(rotation)
            image = image.transformed(transform)

        self.pixmap = QPixmap.fromImage(image)
        self.image_label.setPixmap(self.pixmap)
        self.resizeEvent(None)

    def clear(self):
        """
        Show the image from the provided file_path in the PreviewComponent.
        """
        self.pixmap = QPixmap()
        self.image_label.setPixmap(self.pixmap)
        self.resizeEvent(None)

    def save_as_clicked(self):
        file_dialog = QFileDialog()
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)

        now = datetime.now()
        default_file_name = f"label_{now.strftime('%Y-%m-%d')}.png"

        # Set the default path, if provided
        if Path(Settings.SAVE_AS_PATH).is_dir():
            default_path = Path(Settings.SAVE_AS_PATH, default_file_name)
        else:
            default_path = default_file_name

        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", str(default_path), filter="Image (*.png)")
        file_path = Path(file_path)
        if self.file_path and Path(self.file_path).is_file():
            Settings.SAVE_AS_PATH = str(file_path.parent)
            Settings.save_setting_json()
            shutil.copy(self.file_path, file_path)
            components.main_window.status.show_message(f"Saved {file_path.name} successfully!", "success")

    def resizeEvent(self, event: QResizeEvent) -> None:
        """
        Override the default resizeEvent to resize the displayed image accordingly.
        """
        if event is not None:
            super(PreviewComponent, self).resizeEvent(event)
        if not self.pixmap.isNull():
            w = self.size().width() - 25
            h = self.size().height() - 50
            scaled_pixmap = self.pixmap.scaled(QSize(w, h), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setFixedWidth(w)
            self.image_label.setFixedHeight(h)

            x = self.rect().center().x()
            y = self.rect().center().y()
            self.image_label.move(x - (w // 2), y - (h // 2))
            self.save_as_button.setEnabled(True)
