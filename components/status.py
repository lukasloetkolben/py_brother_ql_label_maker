from PySide6.QtCore import QEvent, QTimer, QPropertyAnimation
from PySide6.QtWidgets import (QHBoxLayout, QFrame, QPushButton, QGraphicsOpacityEffect, QLabel)

import config
from icons import close_icon

class StatusComponent(QFrame):

    def __init__(self):
        super(StatusComponent, self).__init__()
        self.margin = 5

        # Widgets
        self.message_label = QLabel("")
        self.close_button = QPushButton(icon=close_icon, clicked=self.fade_out)
        self.close_button.setFlat(True)

        # Layout
        self.message_layout = QHBoxLayout()
        self.message_layout.setContentsMargins(10, 0, 5, 0)
        self.message_layout.addWidget(self.message_label, 1)
        self.message_layout.addWidget(self.close_button)
        self.setLayout(self.message_layout)

        self.op = QGraphicsOpacityEffect(self)
        self.op.setOpacity(1)
        self.setGraphicsEffect(self.op)

        # Timer
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.fade_out)

        self.hide()

    def fade_out(self):
        if self.isVisible():
            opacity_animation = QPropertyAnimation(self)
            opacity_animation.setTargetObject(self)
            opacity_animation.setDuration(200)
            opacity_animation.setStartValue(1.0)
            opacity_animation.setEndValue(0.0)
            opacity_animation.valueChanged.connect(self.op.setOpacity)
            opacity_animation.finished.connect(self.hide)
            opacity_animation.start()

    def show(self) -> None:
        self.op.setOpacity(1)
        super(StatusComponent, self).show()

    def show_message(self, message, status='error'):
        if status == 'error':
            background_color = config.COLORS.get('red-300')
        elif status == 'warning':
            background_color = config.COLORS.get('yellow-300')
        elif status == 'success':
            background_color = config.COLORS.get('green-300')
        else:
            background_color = config.COLORS.get('gray-300')

        style = f"background-color: {background_color};  border-radius: 4px; color: #FFFFFF;"
        self.setStyleSheet(style)
        self.message_label.setText(message)
        self.message_label.show()
        self.setFixedHeight(35)
        self.update_position()
        self.show()
        self.timer.start(5000)  # hide message after 5 seconds

    def setParent(self, parent):
        super(StatusComponent, self).setParent(parent)
        parent.installEventFilter(self)
        self.update_position()

    def update_position(self):
        margin = 5
        self.setFixedWidth(min(self.parent().rect().width() - margin * 2, 800))
        x = self.parent().rect().center().x() - (self.width() / 2)
        y = self.parent().rect().top() + margin
        if self.parent().menuBar():
            y += self.parent().menuBar().height()
        self.move(x, y)
        self.raise_()

    def eventFilter(self, source, event):
        # ensure that we always cover the whole parent area
        if event.type() == QEvent.Resize:
            self.update_position()

        return super(StatusComponent, self).eventFilter(source, event)
