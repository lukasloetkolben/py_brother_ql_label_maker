#!/usr/bin/env python3

import shutil
from pathlib import Path
import subprocess
import re
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QSplitter, QTabWidget, QComboBox, QLineEdit, QLabel, QWidget, \
    QHBoxLayout, QVBoxLayout, QApplication
from brother_ql.labels import ALL_LABELS
from brother_ql.models import ALL_MODELS

import components
from components.buttons import SuccessButton
from components.icon import Icon
from components.preview import PreviewComponent
from components.status import StatusComponent
from components.tabs.icon_text import IconTextTab
from components.tabs.image import ImageTab
from components.tabs.shipping import ShippingTab
from config import TEMP_DIR
from icons import receipt_long_icon, print_icon
from utilities.printer import get_label_by_name, get_label_by_identifier
from utilities.settings import Settings


class AppWindow(QMainWindow):

    def __init__(self):
        super(AppWindow, self).__init__()
        # Window settings
        self.setWindowTitle("Python Brother QL Label Maker (PBQLLM)")
        self.setGeometry(0, 0, 940, 620)
        self.setWindowState(Qt.WindowState.WindowActive)

        # Widgets
        self.status = StatusComponent()
        self.status.setParent(self)

        self.model_type_select = QComboBox()
        self.model_type_select.addItems([model.name for model in ALL_MODELS])
        self.model_type_select.setCurrentText(Settings.PRINTER_MODEL)
        self.label_type_select = QComboBox()
        self.label_type_select.addItems([label.name for label in ALL_LABELS])
        self.label_type_select.setCurrentText(get_label_by_identifier(Settings.LABEL_TYPE).name)
        self.label_type_select.setFixedWidth(250)
        self.printer_identifier = QLineEdit(Settings.PRINTER_IDENTIFIER)
        self.auto_search_button = SuccessButton("find", clicked=self.on_auto_search_clicked)
        self.save_button = SuccessButton("save", clicked=self.on_save_clicked)
        self.save_button.setEnabled(False)

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setHandleWidth(1)
        self.splitter.setAttribute(Qt.WA_TranslucentBackground)

        self.tabs = QTabWidget()
        self.preview = PreviewComponent(self)

        icon_text = IconTextTab(self)
        self.tabs.addTab(icon_text, "Icon && Text")
        shipping = ShippingTab(self)
        self.tabs.addTab(shipping, "Shipping")
        image = ImageTab(self)
        # self.tabs.addTab(image, "Image")

        # Layouts
        self.splitter.addWidget(self.tabs)
        self.splitter.addWidget(self.preview)
        self.splitter.setSizes([0.5 * self.width(), 0.5 * self.width()])

        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignLeft)
        top_layout.addWidget(Icon(icon=receipt_long_icon))
        top_layout.addWidget(self.label_type_select)
        top_layout.addSpacing(35)
        top_layout.addWidget(Icon(icon=print_icon))
        top_layout.addWidget(self.model_type_select)
        top_layout.addWidget(QLabel("Printer:"))
        top_layout.addWidget(self.printer_identifier)
        top_layout.addWidget(self.auto_search_button)
        top_layout.addWidget(self.save_button)

        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(self.splitter)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Signals
        icon_text.preview_changed.connect(self.on_preview_changed)
        shipping.preview_changed.connect(self.on_preview_changed)
        image.preview_changed.connect(self.on_preview_changed)
        self.label_type_select.currentIndexChanged.connect(self.on_label_type_changed)
        self.model_type_select.currentIndexChanged.connect(self.on_printer_settings_changed)
        self.printer_identifier.textChanged.connect(self.on_printer_settings_changed)

        self.move_to_center()
        self.on_printer_settings_changed()

    def move_to_center(self):
        screen_rect = QApplication.primaryScreen().geometry()
        center_x = screen_rect.center().x()
        center_y = screen_rect.center().y()
        self.move(center_x - self.width() / 2, center_y - self.height() / 2)

    def on_preview_changed(self, image_path: Path, rotation: int):
        if image_path is None:
            self.preview.clear()
        else:
            self.preview.show_image(image_path, rotation)

    def closeEvent(self, event):
        shutil.rmtree(TEMP_DIR)

    def on_label_type_changed(self):
        Settings.LABEL_TYPE = get_label_by_name(self.label_type_select.currentText()).identifier
        Settings.save_setting_json()

    def on_printer_settings_changed(self, *args, **kwargs):
        if not self.printer_identifier.text().strip():
            self.save_button.setEnabled(False)

        elif Settings.PRINTER_IDENTIFIER != self.printer_identifier.text().strip():
            self.save_button.setEnabled(True)

        elif Settings.PRINTER_MODEL != self.model_type_select.currentText():
            self.save_button.setEnabled(True)

        if self.printer_identifier.text().strip():
            self.auto_search_button.hide()
        else:
            self.auto_search_button.show()

    def on_auto_search_clicked(self):
        try:
            lsusb_output = subprocess.check_output(['lsusb']).decode('utf-8')

            for line in lsusb_output.split('\n'):
                if "brother" in line.lower() and "serial" in line.lower():

                    pattern = re.compile(r'ID (\w+:\w+).*Serial: (\w+)')

                    match = pattern.search(line)

                    if match:
                        usb_id = match.group(1)
                        serial_number = match.group(2)
                        self.printer_identifier.setText(f'usb://{usb_id}/{serial_number}')
                        self.save_button.setEnabled(True)

                        for model in [model.name for model in ALL_MODELS]:
                            if model.lower() in line.lower():
                                self.model_type_select.setCurrentText(model)
                                return
        except Exception:
            pass

        self.status.show_message("No Brother Label-Printer found!", "warning")

    def on_save_clicked(self):
        Settings.PRINTER_IDENTIFIER = self.printer_identifier.text().strip()
        Settings.PRINTER_MODEL = self.model_type_select.currentText()
        Settings.save_setting_json()
        self.save_button.setEnabled(False)
