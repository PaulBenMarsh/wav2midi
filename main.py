

def main():

    # from utils import fft

    # print(list(map(abs, fft([1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0]))))

    import sys

    from PyQt5.QtWidgets import QApplication
    from window import MainWindow

    application = QApplication(sys.argv)
    window = MainWindow()

    sys.excepthook = window.excepthook

    window.show()

    return application.exec()

# 
# def main():
# 
#     from utils import WaveFile
# 
#     wave_file = WaveFile()
#     for window in wave_file.iter_window_samples_from_file("440.wav", window_number_of_samples=23):
#         if len(window) != widnow_number_of_samples:
#             break
#         signal_centers = get_signal_centers(window, min_freq=20, max_freq=20000)
#         frame = generate_frame_from_signal_centers(signal_centers)
#         frames.append(frame)
# 
#     update_gui()
# 
#     return 0
# 
# 
# def main1():
#     import wave
#     import struct
#     import cmath
#     from itertools import islice
#     import matplotlib.pyplot as plt
# 
#     with wave.open("440.wav", "rb") as file:
#         number_of_channels = file.getnchannels()
#         bit_depth = file.getsampwidth()
#         sample_rate = file.getframerate()
#         number_of_samples = file.getnframes()
#         samples_as_bytes = file.readframes(number_of_samples)
#         # print(file.getparams())
# 
#     assert number_of_channels == 1
# 
#     samples = struct.unpack("h" * number_of_samples, samples_as_bytes)
#     samples_iter = iter(samples)
# 
#     samples_per_window = 600
# 
#     min_frequency = 20
#     max_frequency = 2000
# 
#     while True:
#         x = []
#         y = []
#         center = 0 + 0j
#         window = list(islice(samples_iter, samples_per_window))
#         if len(window) != samples_per_window:
#             break
#         for index, sample in enumerate(window):
#             result = sample * cmath.exp(2 * cmath.pi * 1j * index * 0.00001)
#             center += result
#             x.append(result.real)
#             y.append(result.imag)
# #         for frequency in range(min_frequency, max_frequency):
# #             pass
#         # plt.plot(list(range(samples_per_window)), window)
#         center /= samples_per_window
#         plt.plot(x, y)
#         plt.plot(center.real, center.imag, marker="o", markersize=3, color="red")
#         plt.show()
#         # break
# 
#     return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
