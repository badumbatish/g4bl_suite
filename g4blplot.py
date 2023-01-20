import matplotlib.pyplot as plt
import numpy as np
import mpl_scatter_density
from os.path import exists

# add feature count
feature_count = 4

# add feature name: x position, y postion and stuff
# can be used for histogram
feature_list = ["x", "y", "Xp", "Yp"]

def add_text_file(file_name):
    # returns a 2D numpy array that formats just like the output txt file from G4Beamline
    if(exists(file_name)):
        data = np.loadtxt(file_name)
    return data

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
        x = data[:,3]
        y = data[:,4]
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

# Set miscellaneous features of a figure
def set_fig_misc(fig, beam_type, plot_type):
    fig.suptitle((f"{beam_type.capitalize()} beam {plot_type}"))
    fig.supxlabel(f"x {plot_type}")
    fig.supylabel(f"y {plot_type}")

# Save the figure into a file, usually pdf
def save_figure(fig, file_name, dpi=300):
    fig.set_size_inches((8.5, 11), forward=False)
    fig.savefig(file_name, dpi=dpi)



