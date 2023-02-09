import g4blplot as plot
import numpy as np
import matplotlib.pyplot as plt

param_dict = {
    "_meanMomentum": [100],
    ("a","b","c"): ([4,5,6],[5,6,7])
    }
if __name__ == '__main__':
    print(plot.generate_args("g4bl",param_dict,"file_name",6))

