import threading
import numpy as np


class SharedRingBuffer:

    def __init__(
        self,
        n_channels,
        capacity,
        dtype=np.float32
    ):

        self.n_channels = n_channels
        self.capacity = capacity

        self.data = np.zeros(
            (capacity, n_channels),
            dtype=dtype
        )

        self._lock = threading.RLock()

        self.write_index = 0

        self.total_samples = 0

    @property
    def sample_index(self):

        return self.total_samples

    def append(self, samples):

        samples = np.asarray(
            samples,
            dtype=self.data.dtype
        )

        if samples.ndim == 1:

            samples = samples.reshape(
                -1,
                self.n_channels
            )

        n = samples.shape[0]

        if n == 0:
            return

        if n >= self.capacity:

            samples = samples[
                -self.capacity:
            ]

            n = self.capacity

        with self._lock:

            start = self.write_index
            end = start + n

            if end <= self.capacity:

                self.data[
                    start:end
                ] = samples

            else:

                first = (
                    self.capacity
                    - start
                )

                self.data[
                    start:
                ] = samples[:first]

                self.data[
                    :n-first
                ] = samples[first:]

            self.write_index = (
                start + n
            ) % self.capacity

            self.total_samples += n

    def get_last(
        self,
        n_samples
    ):

        with self._lock:

            available = min(
                n_samples,
                min(
                    self.total_samples,
                    self.capacity
                )
            )

            if available == 0:

                return np.empty(
                    (
                        0,
                        self.n_channels
                    ),
                    dtype=self.data.dtype
                )

            end = self.write_index

            start = (
                end - available
            ) % self.capacity

            if start < end:

                return self.data[
                    start:end
                ].copy()

            return np.vstack([
                self.data[start:],
                self.data[:end]
            ])

    def get_since(
        self,
        cursor
    ):

        with self._lock:

            current = self.total_samples

            available = (
                current
                - cursor
            )

            overflow = (
                available
                > self.capacity
            )

            if overflow:

                cursor = (
                    current
                    - self.capacity
                )

                available = self.capacity

            if available <= 0:

                return (
                    np.empty(
                        (
                            0,
                            self.n_channels
                        ),
                        dtype=self.data.dtype
                    ),
                    current,
                    False
                )

            start = (
                self.write_index
                - available
            ) % self.capacity

            end = self.write_index

            if start < end:

                data = self.data[
                    start:end
                ].copy()

            else:

                data = np.vstack([
                    self.data[start:],
                    self.data[:end]
                ])

            return (
                data,
                current,
                overflow
            )