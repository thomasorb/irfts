import time
import threading
import h5py
import numpy as np


class RecorderThread(
    threading.Thread
):

    def __init__(
        self,
        buffer,
        filename,
        sample_rate
    ):

        super().__init__(
            daemon=True
        )

        self.buffer = buffer

        self.filename = (
            filename
        )

        self.sample_rate = (
            sample_rate
        )

        self.cursor = 0

        self.running = False

    def stop(self):

        self.running = False

    def run(self):

        self.running = True

        with h5py.File(
            self.filename,
            "w"
        ) as h5:

            h5.attrs[
                "sample_rate"
            ] = self.sample_rate

            h5.attrs[
                "n_channels"
            ] = (
                self.buffer.n_channels
            )

            ds = h5.create_dataset(
                "samples",
                shape=(
                    0,
                    self.buffer.n_channels
                ),
                maxshape=(
                    None,
                    self.buffer.n_channels
                ),
                dtype=np.float32,
                chunks=True
            )

            while self.running:

                data, cursor, overflow = (
                    self.buffer.get_since(
                        self.cursor
                    )
                )

                self.cursor = cursor

                n = data.shape[0]

                if n:

                    old = ds.shape[0]

                    ds.resize(
                        old + n,
                        axis=0
                    )

                    ds[
                        old:old+n
                    ] = data

                time.sleep(
                    0.05
                )