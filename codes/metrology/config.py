# DAQ

LOW_CHANNEL = 0
HIGH_CHANNEL = 3

N_CHANNELS = (
    HIGH_CHANNEL
    - LOW_CHANNEL
    + 1
)

SAMPLE_RATE = 1000

DAQ_BUFFER_SIZE = 10000


# Shared buffer

RING_BUFFER_SIZE = 500000


# Scope

DISPLAY_SAMPLES = 200

SCOPE_REFRESH_HZ = 15

SCOPE_Y_MIN = 0
SCOPE_Y_MAX = 10

# HDF5

DATA_DIRECTORY = "data"


# --------------------------------------------------
# EM (Modulation Efficiency)
# --------------------------------------------------

EM_WINDOW_MIN = 0.1
EM_WINDOW_MAX = 1.0
EM_WINDOW_DEFAULT = 0.5

EM_REFRESH_HZ = 5
