import numpy as np
import config

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout
)

from PyQt6.QtCore import QTimer

from gui.scope_widget import (
    ScopeWidget
)

from gui.control_widget import (
    ControlWidget
)

class MainWindow(
    QMainWindow
):

    def __init__(
        self,
        daq,
        buffer,
        acquisition
    ):

        super().__init__()

        self.daq = daq

        self.buffer = buffer

        self.acquisition = (
            acquisition
        )

        self.recorder = None

        self.setWindowTitle(
            "IRFTS"
        )

        self.resize(
            1600,
            900
        )

        central = QWidget()

        self.setCentralWidget(
            central
        )

        layout = QHBoxLayout(
            central
        )

        self.scope = ScopeWidget(
            self.buffer,
            self.daq,
        )

        self.control = (
            ControlWidget()
        )

        layout.addWidget(
            self.scope,
            stretch=4
        )

        layout.addWidget(
            self.control,
            stretch=1
        )

        self.control.rec_button.clicked.connect(
            self.start_recording
        )

        self.control.stop_button.clicked.connect(
            self.stop_recording
        )

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.update_status
        )

        self.timer.start(500)

        self.em_timer = QTimer()

        self.em_timer.timeout.connect(
            self.update_em
        )

        self.em_timer.start(
            int(
                1000
                / config.EM_REFRESH_HZ
            )
        )


    def update_status(self):

        self.control.sample_label.setText(
            f"Samples : "
            f"{self.buffer.sample_index:,}"
        )

        self.control.overflow_label.setText(
            f"Overflow : "
            f"{self.acquisition.overflow_count}"
        )
        
    def update_em(self):

        window = (
            self.control
            .em_window
            .value()
        )

        n_samples = int(
            window
            * self.daq.sample_rate
        )

        data = self.buffer.get_last(
            n_samples
        )

        if len(data) < 10:
            return

        em_x = (
            self.modulation_efficiency(
                data[:, 0]
            )
        )

        em_y = (
            self.modulation_efficiency(
                data[:, 1]
            )
        )

        if em_x > 0.8:

            color_x = "green"

        elif em_x > 0.5:

            color_x = "orange"

        else:

            color_x = "red"

        if em_y > 0.8:

            color_y = "green"

        elif em_y > 0.5:

            color_y = "orange"

        else:

            color_y = "red"

        # self.control.em_x_label.setText(
        #     f"<font color='{color_x}'>"
        #     f"EM X : {100*em_x:.1f} %"
        #     f"</font>"
        # )

        # self.control.em_y_label.setText(
        #     f"<font color='{color_y}'>"
        #     f"EM Y : {100*em_y:.1f} %"
        #     f"</font>"
        # )

        self.control.em_x.setValue(
            100 * em_x
        )

        self.control.em_y.setValue(
            100 * em_y
        )
    def modulation_efficiency(
        self,
        signal
    ):

        if len(signal) == 0:
            return 0.0

        p99 = np.percentile(
            signal,
            99
        )

        p01 = np.percentile(
            signal,
            1
        )

        if p99 <= 0:
            return 0.0

        return (
            p99 - p01
        ) / p99
        
    def start_recording(self):

        if self.recorder is not None:
            return

        from daq.recorder import (
            RecorderThread
        )

        import datetime
        import pathlib

        filename = (
            pathlib.Path("data")
            /
            datetime.datetime.now().strftime(
                "%Y%m%d_%H%M%S.h5"
            )
        )

        self.recorder = (
            RecorderThread(
                self.buffer,
                filename,
                self.daq.sample_rate
            )
        )

        self.recorder.start()

    def stop_recording(self):

        if self.recorder is None:
            return

        self.recorder.stop()

        self.recorder.join(
            timeout=2
        )

        self.recorder = None

    def closeEvent(
        self,
        event
    ):

        self.stop_recording()

        self.acquisition.stop()

        self.acquisition.join(
            timeout=2
        )

        self.daq.stop_scan()

        self.daq.close()

        event.accept()
