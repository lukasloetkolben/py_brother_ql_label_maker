from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel


class IconTextTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Widgets
        label = QLabel("Icon Text Tab")

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(label)
