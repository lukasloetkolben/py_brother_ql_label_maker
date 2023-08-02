from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QFileDialog, QLineEdit

import components
from components.buttons import PrimaryButton, SecondaryButton, SuccessButton
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
        label = QLabel("Icon Text Tab")
        load_image_button = SecondaryButton("Load icon...", clicked=self.on_load_image_clicked)
        self.text_input = QLineEdit()

        self.create_button = PrimaryButton("Create", clicked=self.on_create_clicked)
        self.print_button = SuccessButton("Print", clicked=self.on_print_clicked)
        self.print_button.setEnabled(False)

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(load_image_button)
        layout.addWidget(self.text_input)
        layout.addWidget(self.create_button)
        layout.addWidget(self.print_button)

    def on_load_image_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.bmp);;All Files (*)")
        if file_path and Path(file_path).is_file():
            self.file_path = Path(file_path)

    def on_create_clicked(self):
        label = get_label_by_identifier(Settings.LABEL_TYPE)
        height, width = label.dots_total
        text = self.text_input.text()
        text_size = 45
        icon_path = self.file_path
        icon_size = 0.8
        self.temp_output_path = create_icon_text_image(width, height, text, text_size, icon_path, icon_size)
        self.preview_changed.emit(self.temp_output_path, 90)
        self.print_button.setEnabled(True)

    def on_print_clicked(self):
        model = Settings.PRINTER_MODEL
        identifier = Settings.PRINTER_IDENTIFIER
        label = Settings.LABEL_TYPE
        output = run_brother_ql_command(model, identifier, label, self.temp_output_path)
        components.main_window.status.show_message(output, "success")

        if output:
            print("Command output:")
            print(output)
