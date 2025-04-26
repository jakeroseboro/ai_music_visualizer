import numpy as np

def detect_kick(fft_chunk):
    low = np.mean(fft_chunk[0:15])
    mids = np.mean(fft_chunk[15:40])
    return low > 5000 and mids < 1000