from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel
)

class ControlWidget(QWidget):

    def __init__(
        self,
        parent=None
    ):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        self.sample_label = QLabel(
            "Samples : 0"
        )

        self.overflow_label = QLabel(
            "Overflow : 0"
        )

        self.rec_button = QPushButton(
            "START REC"
        )

        self.stop_button = QPushButton(
            "STOP REC"
        )

        layout.addWidget(
            self.sample_label
        )

        layout.addWidget(
            self.overflow_label
        )

        layout.addStretch()

        layout.addWidget(
            self.rec_button
        )

        layout.addWidget(
            self.stop_button
        )