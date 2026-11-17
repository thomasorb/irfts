import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets

from IPython.display import display


class Scope:

    def __init__(
        self,
        daq,
        duration=5.0,
        sample_rate=1000,
    ):

        self.daq = daq
        self.sample_rate = sample_rate

        self.n = int(duration * sample_rate)

        # Buffer circulaire logiciel
        self.buffer = np.zeros(
            self.n,
            dtype=np.float64
        )

        self.write_index = 0

        self.running = False
        self.paused = False

        self.total_samples = 0

        self._build_ui()
        self._build_plot()

    # ======================================================
    # UI
    # ======================================================

    def _build_ui(self):

        self.stop_button = widgets.Button(
            description="Stop",
            button_style="danger"
        )

        self.pause_button = widgets.Button(
            description="Pause",
            button_style="warning"
        )

        self.resume_button = widgets.Button(
            description="Resume",
            button_style="success"
        )

        self.status_label = widgets.HTML(
            value="<b style='color:green'>RUNNING</b>"
        )

        self.overflow_label = widgets.HTML(
            value="🟢 Overflow: 0"
        )

        self.samples_label = widgets.HTML(
            value="Samples: 0"
        )

        self.stop_button.on_click(
            self._stop
        )

        self.pause_button.on_click(
            self._pause
        )

        self.resume_button.on_click(
            self._resume
        )

        display(
            widgets.HBox([
                self.stop_button,
                self.pause_button,
                self.resume_button
            ])
        )

        display(
            widgets.HBox([
                self.status_label,
                self.overflow_label,
                self.samples_label
            ])
        )

    # ======================================================
    # PLOT
    # ======================================================

    def _build_plot(self):

        self.fig, self.ax = plt.subplots(
            figsize=(10, 4)
        )

        self.line, = self.ax.plot(
            np.zeros(self.n),
            lw=1,
            color="tab:blue"
        )

        self.ax.grid(True)

        self.ax.set_title(
            "DAQ Scope"
        )

        self.ax.set_xlabel(
            "Samples"
        )

        self.ax.set_ylabel(
            "Voltage (V)"
        )

        plt.show()

    # ======================================================
    # COMMANDS
    # ======================================================

    def _pause(self, _):

        self.paused = True

        self.status_label.value = (
            "<b style='color:orange'>PAUSED</b>"
        )

    def _resume(self, _):

        self.daq.flush()

        self.paused = False

        self.status_label.value = (
            "<b style='color:green'>RUNNING</b>"
        )

    def _stop(self, _):

        self.running = False

        self.status_label.value = (
            "<b style='color:red'>STOPPED</b>"
        )

    # ======================================================
    # BUFFER MANAGEMENT
    # ======================================================

    def append_samples(
        self,
        samples
    ):

        n = len(samples)

        if n == 0:
            return

        if n >= self.n:

            samples = samples[-self.n:]
            n = self.n

        end = self.write_index + n

        if end <= self.n:

            self.buffer[
                self.write_index:end
            ] = samples

        else:

            first = (
                self.n
                - self.write_index
            )

            self.buffer[
                self.write_index:
            ] = samples[:first]

            self.buffer[
                :n-first
            ] = samples[first:]

        self.write_index = (
            self.write_index + n
        ) % self.n

        self.total_samples += n

    def chronological_view(self):

        """
        Retourne le buffer dans l'ordre
        temporel réel.
        """

        idx = self.write_index

        return np.concatenate([
            self.buffer[idx:],
            self.buffer[:idx]
        ])

    # ======================================================
    # DISPLAY
    # ======================================================

    def update_plot(self):

        y = self.chronological_view()

        self.line.set_ydata(
            y
        )

        self.fig.canvas.draw_idle()

    def update_status(
        self,
        overflow
    ):

        self.samples_label.value = (
            f"Samples: "
            f"{self.total_samples:,}"
        )

        if overflow:

            self.overflow_label.value = (
                f"🔴 Overflow: "
                f"{self.daq.overflow_count}"
            )

            self.ax.set_facecolor(
                "#ffe0e0"
            )

        else:

            self.overflow_label.value = (
                f"🟢 Overflow: "
                f"{self.daq.overflow_count}"
            )

            self.ax.set_facecolor(
                "white"
            )

    # ======================================================
    # MAIN LOOP
    # ======================================================

    def run(
        self,
        refresh_hz=20
    ):

        self.running = True

        dt = 1.0 / refresh_hz

        while self.running:

            if self.paused:

                plt.pause(
                    0.05
                )

                continue

            samples, overflow = (
                self.daq.read_new_samples()
            )

            if len(samples):

                self.append_samples(
                    samples
                )

                self.update_plot()

                self.update_status(
                    overflow
                )

            plt.pause(dt)