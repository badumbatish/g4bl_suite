import matplotlib.pyplot as plt
import numpy as np
import mpl_scatter_density
from os.path import exists

# add feature count
feature_count = 4

# add feature name: x position, y postion and stuff
# can be used for histogram
feature_list = ["x", "y", "Xp", "Yp"]

def add_file():
    # returns a 2D numpy array that formats just like the output txt file from G4Beamline
    num_detector = 1
    data = [None] * num_detector
    for i in range(num_detector):
        ascii_output_file =  "detector" + str(i+1) + ".txt"
        if(exists(ascii_output_file)):
            data[i] = np.loadtxt(ascii_output_file)
    return data

data = add_file()

def scatter_plot(axes,data,plot_type = "position", heat_map = False):
    # The second input of data[] is the column
    # 0: x position
    # 1: y position
    # 2: Xp position
    # 3: Yp position
    if plot_type == "position" :
        x = data[:,0]
        y = data[:,1]
    elif plot_type == "momentum" :
        x = data[:,2]
        y = data[:,3]
    if(heat_map == False):
        axes.scatter(x,y, rasterized=False)
    else:
        density = axes.scatter_density(x,y)
        plt.colorbar(density, ax = axes, label='Number of points per pixel')

def hist_plot(axes, data):
    for i in range(4):
        axes[i].hist(data[:,i])
        axes[i].set_xlabel(feature_list[i])
        axes[i].set_xticks

def set_fig_misc(fig, beam_type, plot_type):
    fig.suptitle((f"{beam_type.capitalize()} beam {plot_type}"))
    fig.supxlabel(f"x {plot_type}")
    fig.supylabel(f"y {plot_type}")

def save_figure(fig, file_name, dpi=300):
    fig.set_size_inches((8.5, 11), forward=False)
    fig.savefig(file_name, dpi=dpi)

beam_type = "normal"
plot_type = "position"
use_heat_map = True
gaussian_position_fig, gaussian_position_axes = plt.subplots(1, sharex=True, sharey=True, layout="constrained", subplot_kw=dict(projection="scatter_density"))
set_fig_misc(gaussian_position_fig, beam_type=beam_type, plot_type=plot_type)
scatter_plot(gaussian_position_axes, data[0], heat_map=use_heat_map)
# gaussian_position_axes.set_title("Detector 1 (4mm away from beam source")
save_figure(gaussian_position_fig, f"pics/{beam_type}_position.pdf")

plot_type = "momentum"
gaussian_momentum_fig, gaussian_momentum_axes = plt.subplots(1, sharex=True, sharey=True, layout="constrained", subplot_kw=dict(projection="scatter_density"))
set_fig_misc(gaussian_position_fig, beam_type=beam_type, plot_type=plot_type)

scatter_plot(gaussian_momentum_axes, data[0], plot_type=plot_type, heat_map=use_heat_map)
# gaussian_momentum_axes.set_title("Detector 1 (4mm away from beam source")
save_figure(gaussian_momentum_fig,  f"pics/{beam_type}_momentum.pdf")


gaussian_hist_fig, gaussian_hist_axes = plt.subplots(feature_count, sharey=True, layout="constrained")
gaussian_hist_fig.supylabel("count")
hist_plot(gaussian_hist_axes, data[0])
save_figure(gaussian_hist_fig,f"pics/{beam_type}_hist.pdf")
