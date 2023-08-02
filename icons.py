# Application Icons
import os
from pathlib import Path

from PySide6.QtGui import QIcon, QMovie, QPixmap, QColor, QPainter

from config import BASE, ICONS_DIR, COLORS


def color_icon(icon_path: Path, hex_color):
    pixmap = QPixmap(str(icon_path))

    # PAINTER / PIXMAP
    painter = QPainter(pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), QColor(hex_color))
    painter.end()

    return QIcon(pixmap)


icon_color = COLORS.get("bluegray-900")
close_icon = color_icon(Path(ICONS_DIR, "close_FILL0_wght400_GRAD0_opsz48.svg"), icon_color)
settings_icon = color_icon(Path(ICONS_DIR, "settings_FILL0_wght400_GRAD0_opsz48.svg"), icon_color)

# Animated Gifs
loading_spinner = QMovie(os.path.join(BASE, "assets/images/spinner.gif"))
