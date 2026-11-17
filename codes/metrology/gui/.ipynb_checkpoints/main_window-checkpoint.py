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
            self.buffer
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


    def update_status(self):

        self.control.sample_label.setText(
            f"Samples : "
            f"{self.buffer.sample_index:,}"
        )

        self.control.overflow_label.setText(
            f"Overflow : "
            f"{self.acquisition.overflow_count}"
        )
        
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