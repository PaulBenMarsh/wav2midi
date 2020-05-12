

def find_local_maxima(bins):

    def get_next_maxima_index():

        for i in range(len(bins)):
            try:
                prev_sample = bins[i-1]
                curr_sample = bins[i]
                next_sample = bins[i+1]
            except IndexError:
                continue
            if prev_sample < curr_sample > next_sample:
                yield i

    return list(get_next_maxima_index())


# def naive_dft(window, *, min_freq, max_freq, sample_rate):
# 
#     def get_next_center():
#         import cmath
# 
#         for freq in range(min_freq, max_freq):
#             yield sum([sample * cmath.exp(2 * cmath.pi * 1j * (time / sample_rate) * freq) for time, sample in enumerate(window)]) / len(window)
# 
#     return list(get_next_center())


def fft(window):

    from cmath import exp, pi

    n = len(window)

    if n <= 1:
        return window
    even = fft(window[0::2])
    odd = fft(window[1::2])
    values = [sample * exp(2j * pi * (time / n)) for time, sample in enumerate(odd)]
    return [e + v for e, v in zip(even, values)] + [e - v for e, v in zip(even, values)]


class WaveFile:

    from enum import Enum

    class Channel(Enum):
        Left = 0
        Right = 1

    def __init__(self):
        self.reset()

    def reset(self):
        self.number_of_channels = None
        self.bit_depth = None
        self.sample_rate = None
        self.number_of_samples = None

    def open(self, file_name):
        import wave
        import struct

        bit_depth_to_format = {
            1: "c",
            2: "h",
            4: "i"
        }

        with wave.open(file_name, "rb") as file:
            self.number_of_channels = file.getnchannels()
            self.bit_depth = file.getsampwidth()
            self.sample_rate = file.getframerate()
            self.number_of_frames = file.getnframes()

            try:
                assert self.number_of_channels in (1, 2)
            except AssertionError:
                self.reset()
                raise RuntimeError

            try:
                fmt = bit_depth_to_format[self.bit_depth]
            except KeyError as error:
                self.reset()
                raise error
            else:
                self.samples_as_bytes = file.readframes(self.number_of_frames)
#                 print(f"Number of frames: {self.number_of_frames}")
#                 print(f"Number of channels: {self.number_of_channels}")
#                 print(f"Bit depth: {self.bit_depth}")
#                 print(f"Sample rate: {self.sample_rate}")
#                 print(f"Number of bytes: {len(self.samples_as_bytes)}")
                fmt_string = fmt * self.number_of_frames * self.number_of_channels
                self.interleaved_samples = struct.unpack(fmt_string, self.samples_as_bytes)
                self.left_channel = self.interleaved_samples[0::self.number_of_channels]
                self.right_channel = self.interleaved_samples[1::self.number_of_channels]

    def iter_samples(self, *, channel, sample_window_size):
        from itertools import islice

        try:
            assert isinstance(channel, WaveFile.Channel)
            assert isinstance(sample_window_size, int)
        except AssertionError:
            raise TypeError

        # samples_to_grab = sample_window_size * self.number_of_channels

#         try:
#             assert 0 < sample_window_size <= self.number_of_frames
#         except AssertionError:
#             raise ValueError

        # start = 0
        # stop = samples_to_grab
        # step = self.number_of_channels

        sample_iter = iter([self.left_channel, self.right_channel][self.number_of_channels == 2 and channel is WaveFile.Channel.Right])
        while True:
            samples = list(islice(sample_iter, sample_window_size))
            if len(samples) != sample_window_size:
                break
            yield samples

#     def iter_window_samples_from_file(self, *, number_of_window_samples):
#         import wave
#         import struct
# 
#         with wave.open(self.file_name, "rb") as file:
#             self.number_of_channels = file.getnchannels()
#             self.bit_depth = file.getsampwidth()
#             self.sample_rate = file.getframerate()
#             self.number_of_samples = file.getnframes()
# 
#             assert self.number_of_channels == 1
#             assert self.bit_depth == 2
#             assert self.sample_rate == 44100
# 
#             number_of_samples_remaining = self.number_of_samples
#             while number_of_samples_remaining > 0:
#                 number_of_samples_to_read = min(number_of_window_samples, number_of_samples_remaining)
#                 window_samples_as_bytes = file.readframes(number_of_samples_to_read)
#                 number_of_samples_remaining -= number_of_samples_to_read
#                 samples = struct.unpack("h" * number_of_samples_to_read, window_samples_as_bytes)
#                 yield samples
