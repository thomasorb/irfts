#!/usr/bin/env python3

from PyQt6.QtWidgets import (
    QApplication
)

from config import *

from daq.daq import DAQ

from daq.shared_ring_buffer import (
    SharedRingBuffer
)

from daq.acquisition import (
    AcquisitionThread
)

from gui.main_window import (
    MainWindow
)

def main():

    app = QApplication([])

    daq = DAQ()

    daq.start_scan(
        low_channel=LOW_CHANNEL,
        high_channel=HIGH_CHANNEL,
        sample_rate=SAMPLE_RATE,
        buffer_size=DAQ_BUFFER_SIZE
    )

    ring = SharedRingBuffer(
        n_channels=N_CHANNELS,
        capacity=RING_BUFFER_SIZE
    )

    acquisition = (
        AcquisitionThread(
            daq=daq,
            buffer=ring,
            n_channels=N_CHANNELS
        )
    )

    acquisition.start()

    window = MainWindow(
        daq=daq,
        buffer=ring,
        acquisition=acquisition
    )

    window.show()

    app.exec()

if __name__ == "__main__":

    main()