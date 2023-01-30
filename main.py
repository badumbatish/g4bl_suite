import g4blplot as plot
import numpy as np
import matplotlib.pyplot as plt

param_dict = {
    "_meanMomentum": [100,200,300],
    "_meanXp": [4,5,6,7,8,9]
    }
if __name__ == '__main__':
    plot.automate("/Applications/G4beamline-3.08.app/Contents/MacOS/g4bl", 
                    param_dict=param_dict,
                    file_name = "Pion_Line_BeamEllipse.g4bl",
                    process_count=4,chunksize=4)

