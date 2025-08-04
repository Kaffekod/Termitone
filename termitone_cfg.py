# termitone_cfg.py

# Reference frequencies for the standard EADGBE guitar tuning

STANDARD_TUNING = {
    "E2": 82.41,                # DEFAULT = 82.41
    "A2": 110.00,               # DEFAULT = 110.00
    "D3": 146.83,               # DEFAULT = 146.83
    "G3": 196.00,               # DEFAULT = 196.00
    "B3": 246.94,               # DEFAULT = 246.94
    "E4": 329.63,               # DEFAULT = 329.63
}

# Audio settings
SAMPLE_RATE = 44100             # DEFAULT = 44100 | Sample rate for audio
FRAME_SIZE = 4096               # DEFAULT = 4096 | Number of samples per audio frame, the lower frame size the more responsive, but more inaccurate as a tradeoff
SILENCE_THRESHOLD_DB = -40      # DEFAULT = -40 | Silence threshold in decibels, no need to collect frequencies below 40.

# Tuning feedback settings
PITCH_BUFFER_SIZE = 10          # DEFAULT = 10 | Number of samples used to smooth pitch readings. The lower value the more responsive it gets, but at the cost of accuracy.
PITCH_TOLERANCE = 2.0           # DEFAULT = 2.0 | Tolerance in Hz for "in tune" status. Change it to lower if you want it to be closer to pitch perfect.
BAR_RANGE_HZ = 15.0             # DEFAULT = 15.0 | Frequency range displayed on tuning bar