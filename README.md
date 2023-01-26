Python scripting library for plotting (and analyzing) G4Beamline program ascii output.

This library provides a soft interaction wall between G4Beamline and scientists. 

It doesn't use OOP, only functions. The function mostly manipulates 2D and 1D numpy arrays under the hood and also returns numpy arrays that can be manipulated directly by scientists.

## Dependencies:
    numpy

    mpl-scatter-density: https://github.com/astrofrog/mpl-scatter-density

    matplotlib

## Usage
```python
import g4blplot as plot
import numpy as np
import matplotlib.pyplot as plt


particle_type = "pi-"

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
plot.scatter_plot(pos_axes, x, xp)
plot.save_figure(pos_fig, "position vs angle.pdf")
```