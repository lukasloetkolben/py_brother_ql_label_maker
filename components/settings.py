from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QGridLayout

from components.buttons import SecondaryButton, PrimaryButton
from components.status import StatusComponent


class SettingsDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        # Window
        self.setWindowTitle("Settings")
        self.setGeometry(10, 10, 500, 375)

        # Widgets
        self.cancel_button = SecondaryButton("cancel")
        self.accept_button = PrimaryButton("apply")
        self.accept_button.setDefault(True)

        # Layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.accept_button)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Signals
        self.cancel_button.clicked.connect(self.on_cancel_clicked)
        self.accept_button.clicked.connect(self.on_accept_clicked)

    def on_cancel_clicked(self):
        """
        close current window
        """
        self.close()

    def on_accept_clicked(self):
        """
        accept button clicked
        """
        self.close()