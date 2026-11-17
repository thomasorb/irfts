import atexit
import numpy as np

from uldaq import (
    InterfaceType,
    DaqDevice,
    AiInputMode,
    AInFlag,
    AInScanFlag,
    ScanOption,
    create_float_buffer,
    get_daq_device_inventory,
    Range,
)


class DAQ:

    _RANGE_LIMITS = {

        Range.BIP10VOLTS: (-10.0, 10.0),

        Range.BIP5VOLTS: (-5.0, 5.0),

        Range.BIP2VOLTS: (-2.0, 2.0),

        Range.BIP1VOLTS: (-1.0, 1.0),

        Range.UNI10VOLTS: (0.0, 10.0),

        Range.UNI5VOLTS: (0.0, 5.0),

        Range.UNI2VOLTS: (0.0, 2.0),

        Range.UNI1VOLTS: (0.0, 1.0),
    }


    def __init__(self, device_index=0):

        devices = get_daq_device_inventory(
            InterfaceType.USB
        )

        if not devices:
            raise RuntimeError(
                "No MCC DAQ detected."
            )

        self._daq = DaqDevice(
            devices[device_index]
        )

        self._daq.connect()

        self._ai = self._daq.get_ai_device()

        info = self._ai.get_info()

        print(
            f"Max scan rate : "
            f"{info.get_max_scan_rate()} Hz"
        )

        print(
            f"Min scan rate : "
            f"{info.get_min_scan_rate()} Hz"
        )

        print(
            f"Resolution : "
            f"{info.get_resolution()} bits"
        )

        print(
            f"Pacer : "
            f"{info.has_pacer()}"
        )

        self._input_mode = (
            AiInputMode.SINGLE_ENDED
        )

        self._range = info.get_ranges(
            self._input_mode
        )[0]

        print(
            info.get_ranges(
                self._input_mode
            )
        )
        
        self.sample_rate = None

        self.low_channel = 0
        self.high_channel = 0
        self.n_channels = 1

        self._scan_running = False

        self._scan_buffer = None

        self._scan_size = 0

        self._last_total_count = 0

        self._overflow_count = 0

        atexit.register(
            self.close
        )

    @property
    def device_name(self):

        return (
            self._daq
            .get_descriptor()
            .product_name
        )

    @property
    def range_name(self):

        return str(
            self._range.name
        )

    @property
    def voltage_limits(self):

        return self._RANGE_LIMITS.get(
            self._range,
            (-10.0, 10.0)
        )

    @property
    def overflow_count(self):

        return self._overflow_count

    @property
    def sample_count(self):

        if not self._scan_running:
            return 0

        _, transfer = (
            self._ai.get_scan_status()
        )

        return (
            transfer.current_total_count
        )

    def get_channel(
        self,
        channel
    ):

        return self._ai.a_in(
            channel,
            self._input_mode,
            self._range,
            AInFlag.DEFAULT
        )

    def start_scan(
        self,
        low_channel=0,
        high_channel=0,
        sample_rate=1000,
        buffer_size=10000
    ):

        if self._scan_running:
            return

        self.low_channel = low_channel
        self.high_channel = high_channel

        self.n_channels = (
            high_channel
            - low_channel
            + 1
        )

        self.sample_rate = (
            sample_rate
        )

        self._scan_size = (
            buffer_size
        )

        self._scan_buffer = (
            create_float_buffer(
                self.n_channels,
                buffer_size
            )
        )

        self._last_total_count = 0

        self._ai.a_in_scan(
            self.low_channel,
            self.high_channel,
            self._input_mode,
            self._range,
            buffer_size,
            sample_rate,
            ScanOption.CONTINUOUS,
            AInScanFlag.DEFAULT,
            self._scan_buffer
        )

        self._scan_running = True

    def read_new_samples(self):

        if not self._scan_running:

            return (
                np.empty(
                    (
                        0,
                        self.n_channels
                    ),
                    dtype=np.float32
                ),
                False
            )

        _, transfer = (
            self._ai.get_scan_status()
        )

        current_count = (
            transfer.current_total_count
        )

        current_index = (
            transfer.current_index
        )

        n_new = (
            current_count
            - self._last_total_count
        )

        overflow = False

        if n_new <= 0:

            return (
                np.empty(
                    (
                        0,
                        self.n_channels
                    ),
                    dtype=np.float32
                ),
                False
            )

        if n_new > self._scan_size:

            overflow = True

            self._overflow_count += 1

            n_new = self._scan_size

        buffer = np.ctypeslib.as_array(
            self._scan_buffer,
            shape=(
                self._scan_size
                * self.n_channels,
            ),
        )

        start = (
            current_index
            - (
                n_new
                * self.n_channels
            )
        ) % (
            self._scan_size
            * self.n_channels
        )

        if start < current_index:

            data = buffer[
                start:current_index
            ].copy()

        else:

            data = np.concatenate([
                buffer[start:],
                buffer[:current_index]
            ])

        self._last_total_count = (
            current_count
        )

        data = data.reshape(
            -1,
            self.n_channels
        )

        return (
            data,
            overflow
        )

    def flush(self):

        if not self._scan_running:
            return

        _, transfer = (
            self._ai.get_scan_status()
        )

        self._last_total_count = (
            transfer.current_total_count
        )

    def stop_scan(self):

        if not self._scan_running:
            return

        self._ai.scan_stop()

        self._scan_running = False

    def close(self):

        try:
            self.stop_scan()
        except Exception:
            pass

        try:
            self._daq.disconnect()
        except Exception:
            pass

        try:
            self._daq.release()
        except Exception:
            pass

    def __del__(self):

        self.close()
