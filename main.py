import g4blplot as plot
import numpy as np
import matplotlib.pyplot as plt

param_dict = {
    "_meanMomentum": [100,200],
    "_meanXp": [4,5,6]
    }

plot.automate("/Applications/G4beamline-3.08.app/Contents/MacOS/g4bl", param_dict=param_dict, file_name = "Pion_Line_BeamEllipse.g4bl")