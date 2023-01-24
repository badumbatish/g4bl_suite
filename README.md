Python scripts for plotting (and analyzing) G4Beamline program output

## Dependencies:
    numpy

    mpl-scatter-density: https://github.com/astrofrog/mpl-scatter-density

    matplotlib

## Usage
```python
import g4blplot as plot
import numpy as np
import matplotlib.pyplot as plt


particle_type = "pion-"
use_heat_map = False

# raw data that potentially encompass multiple particles
raw_data = plot.add_text_file("")

# get the data that is only related to pion-
data = plot.extract_particle_data(raw_data, particle_type)

# get the x position and x angle of pion-
x = plot.get_feature(data, 'x')
xp = plot.get_xangle(data)

# make a plot
pos_fig, pos_axes = plt.subplots(1, sharex=True, sharey=True, layout="constrained", subplot_kw=dict(projection="scatter_density"))

# scatter it
pos_axes.scatter(x,xp)
plot.save_figure(pos_fig, "position vs angle.pdf")
```