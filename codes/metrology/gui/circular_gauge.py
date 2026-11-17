from PyQt6.QtCore import (
    Qt,
    QRectF
)

from PyQt6.QtGui import (
    QColor,
    QPainter,
    QPen,
    QFont
)

from PyQt6.QtWidgets import (
    QWidget
)


class CircularGauge(QWidget):

    def __init__(
        self,
        title="EM",
        value=0.0,
        parent=None
    ):
        super().__init__(parent)

        self.title = title
        self.value = float(value)

        self.setMinimumSize(
            150,
            150
        )

    def setValue(
        self,
        value
    ):

        self.value = max(
            0.0,
            min(
                100.0,
                float(value)
            )
        )

        self.update()

    def gauge_color(self):

        if self.value >= 80:
            return QColor("#00C853")

        if self.value >= 50:
            return QColor("#FFB300")

        return QColor("#E53935")

    def paintEvent(
        self,
        event
    ):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        try:

            w = self.width()
            h = self.height()

            size = min(
                w,
                h
            )

            margin = 12

            rect = QRectF(
                margin,
                margin + 15,
                size - 2 * margin,
                size - 2 * margin - 15
            )

            # --------------------------------------------------
            # Fond du disque
            # --------------------------------------------------

            painter.setPen(
                Qt.PenStyle.NoPen
            )

            painter.setBrush(
                QColor("#324A62")
            )

            painter.drawEllipse(rect)

            # --------------------------------------------------
            # Anneau de fond
            # --------------------------------------------------

            ring_width = 10

            pen = QPen(
                QColor("#1F3045"),
                ring_width
            )

            pen.setCapStyle(
                Qt.PenCapStyle.RoundCap
            )

            painter.setPen(pen)

            painter.setBrush(
                Qt.BrushStyle.NoBrush
            )

            start_angle = 225 * 16
            span_angle = -270 * 16

            painter.drawArc(
                rect,
                start_angle,
                span_angle
            )

            # --------------------------------------------------
            # Valeur
            # --------------------------------------------------

            progress_angle = int(
                span_angle
                * self.value
                / 100.0
            )

            pen = QPen(
                self.gauge_color(),
                ring_width
            )

            pen.setCapStyle(
                Qt.PenCapStyle.RoundCap
            )

            painter.setPen(pen)

            painter.drawArc(
                rect,
                start_angle,
                progress_angle
            )

            # --------------------------------------------------
            # Pourcentage
            # --------------------------------------------------

            painter.setPen(
                Qt.GlobalColor.white
            )

            font = QFont()

            font.setBold(True)

            font.setPointSize(18)

            painter.setFont(font)

            painter.drawText(
                rect,
                Qt.AlignmentFlag.AlignCenter,
                f"{self.value:.0f}%"
            )

            # --------------------------------------------------
            # Titre
            # --------------------------------------------------

            title_font = QFont()

            title_font.setBold(True)

            title_font.setPointSize(10)

            painter.setFont(
                title_font
            )

            painter.drawText(
                QRectF(
                    0,
                    0,
                    w,
                    20
                ),
                Qt.AlignmentFlag.AlignCenter,
                self.title
            )

        finally:

            painter.end()
