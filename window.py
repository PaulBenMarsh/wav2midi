
from PyQt5.QtWidgets import QMainWindow, QDialog
from PyQt5.QtCore import pyqtSlot


def resource_path(relative_path):
    import sys
    import os
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class SettingsDialog(QDialog):

    def __init__(self, *args, **kwargs):
        from PyQt5 import uic

        QDialog.__init__(self, *args, **kwargs)

        ui_path = resource_path("resources\\ui\\settings.ui")
        uic.loadUi(ui_path, self)


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        from PyQt5 import uic
        from PyQt5.QtCore import Qt

        from PyQt5.QtWidgets import QHBoxLayout

        import warnings

        QMainWindow.__init__(self, *args, **kwargs)

        ui_path = resource_path("resources\\ui\\main_window.ui")
        uic.loadUi(ui_path, self)

        self.setWindowFlag(Qt.MSWindowsFixedSizeDialogHint)

        warnings.filterwarnings("ignore")

        self.reset_figure()

        # self.axis = self.figure.add_subplot(111, frameon=False)
        # self.figure.tight_layout(rect=[0, 0.1, 1, 1])
        # self.axis.get_yaxis().set_visible(False)
        # self.axis.get_xaxis().set_visible(False)

        layout_frequency = QHBoxLayout()
        layout_frequency.addWidget(self.canvas)
        layout_frequency.setContentsMargins(0, 0, 0, 0)
        self.frame.setLayout(layout_frequency)

        self.wave_file = None

        self.settings = SettingsDialog()

        self.disable()

    def reset_figure(self):
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
        from matplotlib.figure import Figure

        self.figure = Figure(facecolor="#d4d0c8")
        self.canvas = FigureCanvas(self.figure)

    @pyqtSlot()
    def on_action_open_triggered(self):
        from PyQt5.QtWidgets import QFileDialog
        from utils import WaveFile

        dialog = QFileDialog()
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setNameFilter("Wave File (*.wav)")
        if dialog.exec() == QFileDialog.Accepted:
            self.disable()
            # self.reset_figure()
            file_path = dialog.selectedFiles()[0]
            self.wave_file = WaveFile()
            self.wave_file.open(file_path)
            self.enable()

    @pyqtSlot()
    def on_action_settings_triggered(self):
        self.settings.exec()

    @pyqtSlot()
    def on_action_generate_triggered(self):

        from utils import WaveFile, fft, find_local_maxima

        from math import sqrt

        from matplotlib import animation

        if self.wave_file is None:
            return

        # sample_window_size = self.settings.spin_resolution.value() * 2
        sample_window_size = 2 ** 14
        bin_width = self.wave_file.sample_rate / sample_window_size
        # desired_freq = 440
        # xlim_pad = 60
        # xlim = ((desired_freq / bin_width) - xlim_pad, (desired_freq / bin_width) + xlim_pad)
        # print(f"Bin width: {bin_width}hz")
        # print(f"Bin number @ {desired_freq}hz: {desired_freq / bin_width}")
        
        

        axis = self.figure.add_subplot(111, frameon=False)
        self.figure.tight_layout(rect=[0, 0.1, 1, 1])
        axis.get_yaxis().set_visible(False)
        axis.clear()
# 
#         def update(data):
#             line = axis.get_line()
#             line.set_ydata(data)
#             return line
# 
#         def data_gen():
#             channel = WaveFile.Channel.Left
#             for window in self.wave_file.iter_samples(channel=channel, sample_window_size=sample_window_size):
#                 bins = fft(window)
#                 # magnitudes_x = [bin_width * _ for _ in range(sample_window_size)]
#                 magnitudes_y = [sqrt(c.imag ** 2 + c.real ** 2) for c in bins]
#                 yield magnitudes_y
# 
#         ani = animation.FuncAnimation(self.figure, update, data_gen, interval=500)
#         self.canvas.draw()

        for window in self.wave_file.iter_samples(channel=WaveFile.Channel.Left, sample_window_size=sample_window_size):
            bins = fft(window)
            magnitudes_x = [bin_width * _ for _ in range(sample_window_size)]
            magnitudes_y = [sqrt(c.imag * c.imag + c.real * c.real) for c in bins]
            # imags = [c.imag for c in bins]
 
            # maxima_x = find_local_maxima(magnitudes)
            # maxima_y = [magnitudes[i] for i in maxima_x]
            # print(maxima_y[0:4])
 
            axis = self.figure.add_subplot(111, frameon=False)
            self.figure.tight_layout(rect=[0, 0.1, 1, 1])
            axis.get_yaxis().set_visible(False)
            axis.clear()
            axis.plot(magnitudes_x, magnitudes_y, "-", linewidth=1)
            # axis.plot(imags, "-", linewidth=1)
            # axis.plot(maxima_x, maxima_y, "go")
            # axis.set_xlim(*xlim)
            axis.set_xlim(0, sample_window_size)
            self.canvas.draw()
            break
# 
#         min_freq = self.settings.spin_min_freq.value()
#         max_freq = self.settings.spin_max_freq.value()
#         sample_window_size = self.settings.spin_resolution.value()
# 
#         for window in self.wave_file.iter_samples(channel=WaveFile.Channel.Left, sample_window_size=sample_window_size):
#             centers = get_window_centers(window, min_freq=min_freq, max_freq=max_freq, sample_rate=self.wave_file.sample_rate)
#             x = list(range(min_freq, max_freq))
#             y = [c.imag for c in centers]
# 
#             axis = self.figure.add_subplot(111, frameon=False)
#             self.figure.tight_layout(rect=[0, 0.1, 1, 1])
#             axis.get_yaxis().set_visible(False)
#             axis.clear()
#             axis.plot(x, y, "-", linewidth=1)
#             self.canvas.draw()
#             break

        # y = self.wave_file.left_channel

#         axis = self.figure.add_subplot(111, frameon=False)
#         self.figure.tight_layout(rect=[0, 0.1, 1, 1])
#         axis.get_yaxis().set_visible(False)
        # self.axis.clear()
        # self.axis.plot(y, "-", linewidth=1)
        # self.canvas.draw()


        # for samples in self.wave_file.iter_samples(channel=WaveFile.Channel.Left, sample_window_size=4096):
            
            
        
#         from utils import get_signal_centers
# 
#         if self.wave_file is None:
#             return
#         min_freq = self.settings.spin_min_freq.value()
#         max_freq = self.settings.spin_max_freq.value()
#         number_of_window_samples = self.settings.spin_resolution.value()
#         for window in self.wave_file.iter_window_samples_from_file(number_of_window_samples=number_of_window_samples):
#             if len(window) != number_of_window_samples:
#                 break
#             centers = get_signal_centers(window, min_freq=min_freq, max_freq=max_freq)
#             x = list(range(min_freq, max_freq))
#             # y = [center.imag for center in centers]
#             axis = self.figure.add_subplot(111, frameon=False)
#             self.figure.tight_layout(rect=[0, 0.1, 1, 1])
#             axis.get_yaxis().set_visible(False)
#             axis.clear()
#             axis.plot(x, centers, "-", linewidth=1)
#             self.canvas.draw()
#             break

#         from random import randint
# 
#         data = [randint(0, 10) for _ in range(10)]
#         axis = self.figure.add_subplot(111, frameon=False)
#         self.figure.tight_layout(rect=[0, 0.1, 1, 1])
#         axis.get_yaxis().set_visible(False)
#         axis.clear()
#         axis.plot(data, "-")
#         self.canvas.draw()

    def enable(self):
        self.set_widgets_enabled(True)

    def disable(self):
        self.set_widgets_enabled(False)
        self.slider.maximum = 99
        self.slider.singleStep = 1
        self.wave_file = None
        self.wave_file_path = None

    def set_widgets_enabled(self, state):
        self.menu_dft.setEnabled(state)
        self.tab_widget.setEnabled(state)
        self.button_play.setEnabled(state)
        self.button_stop.setEnabled(state)
        self.slider.setEnabled(state)
        self.slider.value = 0
        self.slider.sliderPosition = 0
        self.plain_text_log.setEnabled(state)
        self.progress_bar.setEnabled(state)

    def excepthook(self, exctype, value, traceback):
        print(exctype, value, traceback.tb_frame, traceback.tb_lasti, traceback.tb_lineno, traceback.tb_next)
