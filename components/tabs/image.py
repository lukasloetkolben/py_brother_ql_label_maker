from pathlib import Path

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget, QLabel, QFileDialog, QGridLayout, QSpacerItem, QVBoxLayout, \
    QGraphicsView, QGraphicsScene

from components.buttons import SecondaryButton


class ImageTab(QWidget):
    preview_changed = Signal(object, int)  # filepath, rotation

    def __init__(self, parent):
        super().__init__(parent)
        # Variables
        self.file_path = None  # file path of selected image
        self.temp_output_path = None

        # Widgets
        self.file_path_label = QLabel("")
        load_icon_button = SecondaryButton("Load Image...", clicked=self.on_load_image_clicked)

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.view.setUpdatesEnabled(True)
        self.view.setMouseTracking(True)

        # Layout
        layout = QGridLayout()
        layout.addWidget(self.file_path_label, 0, 0, 1, 5)
        layout.addWidget(load_icon_button, 1, 0, 1, 6)
        layout.addItem(QSpacerItem(30, 30), 2, 0)

        QVBoxLayout(self)
        self.layout().setAlignment(Qt.AlignVCenter)
        dummy = QLabel("Not working dummy tab!")
        dummy.setAlignment(Qt.AlignHCenter)
        dummy.setStyleSheet("color:red;")
        self.layout().addWidget(dummy)
        self.layout().addWidget(self.view)
        self.layout().addLayout(layout)

    def on_load_image_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.bmp);;All Files (*)")
        if file_path and Path(file_path).is_file():
            self.file_path = Path(file_path)
            self.file_path_label.setText(str(self.file_path))

    def on_create_clicked(self):
        pass

    def on_print_clicked(self):
        pass
