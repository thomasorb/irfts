import time
import threading
import numpy as np


class AcquisitionThread(
    threading.Thread
):

    def __init__(
        self,
        daq,
        buffer,
        n_channels=1
    ):

        super().__init__(
            daemon=True
        )

        self.daq = daq
        self.buffer = buffer

        self.n_channels = (
            n_channels
        )

        self.running = False

        self.overflow_count = 0

    def stop(self):

        self.running = False

    def run(self):

        self.running = True

        while self.running:

            samples, overflow = (
                self.daq.read_new_samples()
            )

            if overflow:

                self.overflow_count += 1

            if len(samples):

                samples = np.asarray(
                    samples,
                    dtype=np.float32
                )

                samples = samples.reshape(
                    -1,
                    self.n_channels
                )

                self.buffer.append(
                    samples
                )

            time.sleep(
                0.001
            )