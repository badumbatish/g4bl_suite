Python scripts for plotting (and analyzing) G4Beamline program output

## Dependencies:
    numpy

    mpl-scatter-density: https://github.com/astrofrog/mpl-scatter-density

    matplotlib

## Usage:
```python
import g4blplot as plot

# Reads txt file data
data = plot.add_text_file("file_name.txt")

# Create the figure with axes
fig, axes = plt.subplots(1, sharex=True, sharey=True, layout="constrained", subplot_kw=dict(projection="scatter_density"))

# Scatter plot the x position versus the y position of a particle
plot.scatter_plot(axes, data, x_axis = 'x', y_axis = 'y', heat_map = False)

# Histogram plot
# Create a new figure for histogram plotting
hist_fig, hist_axes = plt.subplots(4, sharey=True, layout="constrained")

# Histogram plot
plot.hist_plot(hist_axes, data)
```

