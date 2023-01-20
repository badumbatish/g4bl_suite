import g4blplot
import numpy as np
import matplotlib.pyplot as plt

beam_type = "negative_ellipse"
plot_type = "position"
particle_type = "mu-"
use_heat_map = False

# raw data that potentially encompass multiple particles
raw_data = g4blplot.add_text_file(f"{beam_type}_detector_8.txt")

# mu-, PID = 13
# pi-, PID = -211

# make a 1D array mask that returns true if the PID is satisfy
# [:,7] represents the column of PIDs
mask = (raw_data[:,7] == 13)

# pass the mask to the raw data to select the PID-satisfying rows, then : to select all the columns of that row
data = raw_data[mask,:]
particle_count = np.size(data,0)
events = 100000
print(f"Particle count: {particle_count} mu- make it out of initial {events} pions-")
