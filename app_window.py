#!/usr/bin/env python3

import shutil
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QSplitter, QTabWidget
from PySide6.QtWidgets import QMenu

from components.preview import PreviewComponent
from components.settings import SettingsDialog
from components.status import StatusComponent
from components.tabs.icon_text import IconTextTab
from components.tabs.shipping import ShippingTab
from config import TEMP_DIR


class AppWindow(QMainWindow):

    def __init__(self):
        super(AppWindow, self).__init__()
        # Window settings
        self.setWindowTitle("Python Brother QL Label Maker (PyBQLLM)")
        self.setGeometry(0, 0, 800, 600)
        self.setWindowState(Qt.WindowState.WindowActive)

        # Menubar
        menubar = self.menuBar()
        file = QMenu("File", self)
        menubar.addMenu(file)
        settings_button = QAction("Settings", self)
        settings_button.triggered.connect(self.on_settings_clicked)
        file.addAction(settings_button)

        # Widgets
        self.status_widget = StatusComponent()
        self.status_widget.setParent(self)

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setHandleWidth(1)
        self.splitter.setAttribute(Qt.WA_TranslucentBackground)

        self.tabs = QTabWidget()
        self.preview = PreviewComponent(self)

        # Add the tabs to the tab widget
        self.tabs.addTab(IconTextTab(), "Icon & Text")
        self.tabs.addTab(ShippingTab(), "Shipping")


        # Dialogs
        self.settings_form = SettingsDialog(self)

        # Layouts
        self.splitter.addWidget(self.tabs)
        self.splitter.addWidget(self.preview)
        self.setCentralWidget(self.splitter)

        # Signals

    def closeEvent(self, event):
        shutil.rmtree(TEMP_DIR)

    def on_settings_clicked(self):
        self.settings_form.exec()