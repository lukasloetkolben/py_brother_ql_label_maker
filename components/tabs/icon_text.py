from pathlib import Path

from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QWidget, QLabel, QFileDialog, QLineEdit, QGridLayout, QSpacerItem, QVBoxLayout, QComboBox, \
    QSlider

import components
from components.buttons import PrimaryButton, SecondaryButton, SuccessButton, DangerButton
from utilities.images import create_icon_text_image
from utilities.printer import run_brother_ql_command, get_label_by_identifier
from utilities.settings import Settings


class IconTextTab(QWidget):
    preview_changed = Signal(object, int)  # filepath, rotation

    def __init__(self, parent):
        super().__init__(parent)
        # Variables
        self.file_path = None  # file path of selected image
        self.temp_output_path = None

        # Widgets
        self.file_path_label = QLabel("")
        load_icon_button = SecondaryButton("Load Icon...", clicked=self.on_load_image_clicked)
        self.clear_file_path_button = DangerButton("x", clicked=self.on_clear_file_path_clicked)
        self.clear_file_path_button.setFixedWidth(25)
        self.clear_file_path_button.hide()
        self.icon_rotation_input = QLineEdit()
        self.icon_size = QSlider(Qt.Horizontal)
        self.icon_size.setMinimum(10)
        self.icon_size.setMaximum(200)
        self.icon_size.setValue(80)

        self.text_input = QLineEdit()
        self.secondary_text_input = QLineEdit()
        self.fonts = QComboBox()
        self.fonts.addItems(["Arial"])
        self.text_rotation_input = QLineEdit()
        self.font_size = QSlider(Qt.Horizontal)
        self.font_size.setMinimum(5)
        self.font_size.setMaximum(250)
        self.font_size.setValue(45)

        self.create_button = PrimaryButton("Create", clicked=self.on_create_clicked)
        self.print_button = SuccessButton("Print", clicked=self.on_print_clicked)
        self.print_button.setEnabled(False)

        # Layout
        layout = QGridLayout()
        layout.addWidget(self.file_path_label, 0, 0, 1, 4)
        layout.addWidget(self.clear_file_path_button, 0, 5)
        layout.addWidget(load_icon_button, 1, 0, 1, 6)
        layout.addWidget(QLabel("Icon Rotation:"), 2, 0)
        layout.addWidget(self.icon_rotation_input, 2, 1, 1, 5)
        layout.addWidget(QLabel("Icon Size:"), 3, 0)
        layout.addWidget(self.icon_size, 3, 1, 1, 5)
        layout.addItem(QSpacerItem(30, 30), 4, 0)
        layout.addWidget(QLabel("Text:"), 5, 0)
        layout.addWidget(self.text_input, 5, 1, 1, 5)
        layout.addWidget(QLabel("Font:"), 6, 0)
        layout.addWidget(self.fonts, 6, 1, 1, 5)
        layout.addWidget(QLabel("Text Rotation:"), 7, 0)
        layout.addWidget(self.text_rotation_input, 7, 1, 1, 5)
        layout.addWidget(QLabel("Font Size:"), 8, 0)
        layout.addWidget(self.font_size,8, 1, 1, 5)
        layout.addItem(QSpacerItem(30, 30), 9, 0)
        layout.addWidget(self.create_button, 10, 4)
        layout.addWidget(self.print_button, 10, 5)

        QVBoxLayout(self)
        self.layout().setAlignment(Qt.AlignVCenter)
        self.layout().addLayout(layout)

    def on_clear_file_path_clicked(self):
        self.file_path = None
        self.file_path_label.setText("")
        self.preview_changed.emit(None, 0)
        self.clear_file_path_button.hide()
        self.on_create_clicked()

    def on_load_image_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.bmp);;All Files (*)")
        if file_path and Path(file_path).is_file():
            self.file_path = Path(file_path)
            self.file_path_label.setText(str(self.file_path))
            self.clear_file_path_button.show()

    def on_create_clicked(self):
        label = get_label_by_identifier(Settings.LABEL_TYPE)
        height, width = label.dots_printable
        text = self.text_input.text()
        text_rotation = int(self.text_rotation_input.text())
        font_size = int(self.font_size.value())
        font_family = self.fonts.currentText()
        icon_path = self.file_path
        icon_rotation = int(self.icon_rotation_input.text())
        icon_size = self.icon_size.value() / 100.0
        self.temp_output_path = create_icon_text_image(width, height, text, text_rotation, font_size, font_family, icon_path,icon_rotation, icon_size)
        self.preview_changed.emit(self.temp_output_path, 90)
        self.print_button.setEnabled(True)

    def on_print_clicked(self):
        self.on_create_clicked()
        model = Settings.PRINTER_MODEL
        identifier = Settings.PRINTER_IDENTIFIER
        label = Settings.LABEL_TYPE
        output = run_brother_ql_command(model, identifier, label, self.temp_output_path)
        components.main_window.status.show_message(output, "success")
