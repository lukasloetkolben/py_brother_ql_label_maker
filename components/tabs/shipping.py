from pathlib import Path

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget, QLabel, QFileDialog, QGridLayout, QSpacerItem, QVBoxLayout, QComboBox

import components
from components.buttons import PrimaryButton, SecondaryButton, SuccessButton, DangerButton
from utilities.printer import run_brother_ql_command, get_label_by_identifier
from utilities.settings import Settings
from utilities.shipping import shipping_companies


class ShippingTab(QWidget):
    preview_changed = Signal(object, int)  # filepath, rotation

    def __init__(self, parent):
        super().__init__(parent)
        # Variables
        self.file_path = None  # file path of selected image
        self.temp_output_path = None
        self.created_labe_type = None

        # Widgets
        self.notice_label = QLabel("Shipping labels can only be printed on 102x152mm labels!")
        self.notice_label.hide()
        self.notice_label.setAlignment(Qt.AlignHCenter)

        self.shipping_company = QComboBox()
        self.shipping_company.addItems(list(shipping_companies.keys()))

        self.file_path_label = QLabel("")

        load_shipping_label_button = SecondaryButton("Load PDF...", clicked=self.on_load_shipping_label_clicked)
        self.clear_file_path_button = DangerButton("x", clicked=self.on_clear_file_path_clicked)
        self.clear_file_path_button.setFixedWidth(25)
        self.clear_file_path_button.hide()

        self.create_button = PrimaryButton("Create", clicked=self.on_create_clicked)
        self.print_button = SuccessButton("Print", clicked=self.on_print_clicked)
        self.print_button.setEnabled(False)

        # Layout
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        layout.addWidget(self.notice_label, 0, 0, 1, 5)
        layout.addItem(QSpacerItem(50, 50), 1, 0)
        layout.addWidget(QLabel("Shipping Company"), 2, 1, Qt.AlignLeft)
        layout.addWidget(self.shipping_company, 2, 2, 1, 2, Qt.AlignLeft)
        layout.addWidget(self.file_path_label, 3, 0, 1, 4, Qt.AlignLeft)
        layout.addWidget(self.clear_file_path_button, 3, 4, Qt.AlignRight)
        layout.addWidget(load_shipping_label_button, 4, 0, 1, 5)
        layout.addItem(QSpacerItem(30, 30), 5, 0)
        layout.addWidget(self.create_button, 6, 3)
        layout.addWidget(self.print_button, 6, 4)

        QVBoxLayout(self)
        self.layout().setAlignment(Qt.AlignHCenter)
        self.layout().addLayout(layout)

    def on_clear_file_path_clicked(self):
        self.file_path = None
        self.file_path_label.setText("")
        self.preview_changed.emit(None, 0)
        self.clear_file_path_button.hide()
        self.on_create_clicked()

    def on_load_shipping_label_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Shipping Label", "", "Document (*.pdf);;All Files (*)")
        if file_path and Path(file_path).is_file():
            self.file_path = Path(file_path)
            self.file_path_label.setText(str(self.file_path))
            self.clear_file_path_button.show()

    def on_create_clicked(self):
        create_label_func = shipping_companies.get(self.shipping_company.currentText())
        label, self.temp_output_path = create_label_func(get_label_by_identifier(Settings.LABEL_TYPE), self.file_path)

        if label and self.temp_output_path and self.temp_output_path.is_file():
            self.preview_changed.emit(self.temp_output_path, 0)
            self.print_button.setEnabled(True)
        else:
            components.main_window.status.show_message("Something went wrong. Please try again!", "error")

        if label and label != get_label_by_identifier(Settings.LABEL_TYPE):
            self.notice_label.show()
        else:
            self.notice_label.hide()

    def on_print_clicked(self):
        model = Settings.PRINTER_MODEL
        identifier = Settings.PRINTER_IDENTIFIER
        label = Settings.LABEL_TYPE
        output = run_brother_ql_command(model, identifier, label, self.temp_output_path)
        components.main_window.status.show_message(output, "success")
