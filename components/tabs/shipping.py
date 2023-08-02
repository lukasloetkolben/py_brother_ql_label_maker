from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel


class ShippingTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        # Widgets
        label = QLabel("Shipping Tab")

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(label)
