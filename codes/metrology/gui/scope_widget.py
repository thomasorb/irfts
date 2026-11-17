from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QVBoxLayout

import pyqtgraph as pg

import numpy as np

import config

CHANNEL_NAMES = [
    "HeNe X",
    "HeNe Y",
    "Science A",
    "Science B"
]

class ScopeWidget(QWidget):

    def __init__(
        self,
        buffer,
        daq,
        parent=None
    ):

        super().__init__(parent)

        self.buffer = buffer
        self.daq = daq
        
        self.n_channels = (
            buffer.n_channels
        )

        self.layout = QVBoxLayout(self)

        self.graphics = (
            pg.GraphicsLayoutWidget()
        )

        self.layout.addWidget(
            self.graphics
        )

        self.plots = []
        self.curves = []

        colors = [
            "#00ff00",
            "#00ffff",
            "#ffff00",
            "#ff00ff"
        ]

        ymin, ymax = (
            [config.SCOPE_Y_MIN, config.SCOPE_Y_MAX]
        )
        
        for ch in range(
            self.n_channels
        ):

            plot = (
                self.graphics.addPlot(
                    row=ch,
                    col=0
                )
            )

            plot.disableAutoRange(
                axis='y'
            )

            plot.setYRange(
                ymin,
                ymax
            )
            
            plot.showGrid(
                x=True,
                y=True
            )

            plot.setLabel(
                "left",
                f"CH{ch}"
            )

            plot.setTitle(
                CHANNEL_NAMES[ch]
            )

            if ch == (
                self.n_channels - 1
            ):
                plot.setLabel(
                    "bottom",
                    "Samples"
                )

            curve = plot.plot(
                pen=pg.mkPen(
                    colors[
                        ch % len(colors)
                    ],
                    width=1
                )
            )

            self.plots.append(
                plot
            )

            self.curves.append(
                curve
            )

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.refresh
        )

        self.timer.start(
            int(
                1000 / config.SCOPE_REFRESH_HZ
            )
        )

    def refresh(self):

        data = self.buffer.get_last(
            config.DISPLAY_SAMPLES
        )

        if len(data) == 0:
            return

        n = data.shape[0]

        x = np.arange(n)

        for ch in range(
            self.n_channels
        ):

            self.curves[ch].setData(
                x,
                data[:, ch]
            )
