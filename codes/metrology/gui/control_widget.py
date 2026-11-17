from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QDoubleSpinBox
)

from gui.circular_gauge import (
    CircularGauge
)

import config


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

        layout.addWidget(
            self.sample_label
        )

        layout.addWidget(
            self.overflow_label
        )

        # ----------------------------------
        # EM
        # ----------------------------------

        layout.addWidget(
            QLabel(
                "EM Window"
            )
        )

        self.em_window = (
            QDoubleSpinBox()
        )

        self.em_window.setMinimum(
            config.EM_WINDOW_MIN
        )

        self.em_window.setMaximum(
            config.EM_WINDOW_MAX
        )

        self.em_window.setSingleStep(
            0.1
        )

        self.em_window.setValue(
            config.EM_WINDOW_DEFAULT
        )

        self.em_window.setSuffix(
            " s"
        )

        layout.addWidget(
            self.em_window
        )

        self.em_x = CircularGauge(
            "HeNe X"
        )
        
        self.em_y = CircularGauge(
            "HeNe Y"
        )

        layout.addWidget(
            self.em_x
        )
        
        layout.addWidget(
            self.em_y
        )

        # self.em_x_label = QLabel(
        #     "EM X : --- %"
        # )

        # self.em_y_label = QLabel(
        #     "EM Y : --- %"
        # )

        # layout.addWidget(
        #     self.em_x_label
        # )

        # layout.addWidget(
        #     self.em_y_label
        # )

        layout.addStretch()

        self.rec_button = QPushButton(
            "START REC"
        )

        self.stop_button = QPushButton(
            "STOP REC"
        )

        layout.addWidget(
            self.rec_button
        )

        layout.addWidget(
            self.stop_button
        )
