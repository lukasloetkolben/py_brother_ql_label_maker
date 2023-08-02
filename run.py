#!/usr/bin/env python3

import os
import sys
import components
from PySide6.QtCore import Qt
from PySide6.QtQuick import QQuickWindow, QSGRendererInterface
from PySide6.QtWidgets import QApplication

from config import COLORS, CONFIG_DIR, TEMP_DIR, STYLE
from utilities.settings import Settings


def apply_style(style_sheet):
    css = open(style_sheet, "r").read()

    for key, value in COLORS.items():
        css = css.replace(key, value)

    return css


if __name__ == '__main__':
    # create necessary folders
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    Settings.read_setting_json()
    os.environ["QT_FONT_DPI"] = str(Settings.DPI)

    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    if sys.platform == 'darwin':
        QApplication.setAttribute(Qt.AA_DontUseNativeMenuBar)
        QQuickWindow.setGraphicsApi(QSGRendererInterface.OpenGL)

    QApplication.setQuitOnLastWindowClosed(True)
    qapp = QApplication(sys.argv)
    qapp.setStyleSheet(apply_style(STYLE))

    from components.app_window import AppWindow
    a = AppWindow()
    components.main_window = a
    a.show()

    qapp.exec()
