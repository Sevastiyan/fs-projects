from scipy.signal import butter, filtfilt


def butter_lowpass_filter(signal, cutoff=5, fs=20, order=4):
    """Return a low-pass filtered signal."""
    nyq = 0.5 * fs  # Nyquist frequency
    normal_cutoff = cutoff / nyq  # Normalize the cutoff
    b, a = butter(order, normal_cutoff, btype='low',
                  analog=False)  # Filter coefficients
    y = filtfilt(b, a, signal)  # Filter the signal
    return y


def butter_highpass_filter(signal, cutoff, fs, order=3):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    y = filtfilt(b, a, signal)
    return y


def butter_bandpass_filter(signal, lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    y = filtfilt(b, a, signal)
    return y