import matplotlib.pyplot as plt
import numpy as np
import mpl_scatter_density
from os.path import exists


feature_list = ["x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "TrackID", "ParentID", "Weight"]
feature_dict = {key : value for (value,key) in enumerate(feature_list)} 

particle_dict = {"pi-": -211,
                "mu-": 13,
                "mu+": -13}

def add_text_file(file_name):
    """Returns a 2D numpy array that formats just like the output txt file from G4Beamline and raise exception if file does not exists

    Parameters
    ----------
    file_name: str

    Returns
    ----------
    data
        a 2D numpy array
    """

    if(exists(file_name)):
        data = np.loadtxt(file_name)
        return data
    else:
        raise Exception(f"The file {file_name} does not exist")

def scatter_plot(axes, x_axis, y_axis, heat_map = False):
    """ Scatter plot an axes based on 2 1D numpy array
    Parameters
    ----------
    axes : 
        an object subplot from matplotlib that is a  
    x_axis : 
        1D array that denotes what to plot on the x axis
    y_axis : 
        1D arra that denotes what to plot on the y axis

    Returns
    ----------
        Function returns nothing, only plots a graph to the axes
    """

    if(heat_map == False):
        axes.scatter(x_axis,y_axis, rasterized=False)
    else:
        density = axes.scatter_density(x_axis,y_axis)
        plt.colorbar(density, ax = axes, label='Number of points per pixel')

def hist_plot(axes, data, xlabel=None):
    """
        This function plots histogram in the axes

    Parameters
    ----------
    axes : an axe plot

    data : a 1D numpy array

    Returns:
    A historgram plot with extra descriptive data of count, mean, std, min, 25,50,75 percentile, and max.
    ----------
    """
    axes.hist(data)
    if xlabel is not None:
        axes.set_xlabel(xlabel)
        axes.set_ylabel(f"Count of {xlabel}")
    stats_str = f"Count: {data.size}\nMean: {data.mean():.3f}\nStd: {data.std():.3f}\nMin: {data.min()}\n25%: {np.percentile(data,25)}\n50%: {np.percentile(data,50)}\n75%: {np.percentile(data,75)}\nMax: {data.max()}"
    axes.text(1.01,0.2, stats_str ,transform=plt.gca().transAxes)

def set_fig_misc(fig, beam_type, plot_type):
    """Sets miscellaneous features of a figure

    Parameters
    ----------
    fig :

    beam_type :

    plot_type :
    Returns
    ----------
    """
    fig.suptitle((f"{beam_type.capitalize()} beam {plot_type}"))
    fig.supxlabel(f"x {plot_type}")
    fig.supylabel(f"y {plot_type}")

def save_figure(fig, file_name, dpi=300):
    """Save the figure into a file, usually pdf
    """
    fig.set_size_inches((8.5, 11), forward=False)
    fig.savefig(file_name, dpi=dpi)

def extract_particle_data(numpy_array, particle_name):
    """Extracts a numpy array of only a certain particle out of a raw data

    Parameters
    ----------

    Returns
    ----------
    """
    # make a 1D array mask that returns true if the PID is satisfy
    # [:,7] represents the column of PIDs
    mask = (numpy_array[:,feature_dict["PDGid"]] == particle_dict[particle_name])

    # pass the mask to the raw data to select the PID-satisfying rows, then : to select all the columns of that row
    particle_data = numpy_array[mask,:]

    return particle_data

def get_feature(data, feature_name):
    return data[:,feature_dict[feature_name]]
    
def get_xangle(data):
    """
        This function returns a 1D array consisting of xp = Px/Pz in milliradian
    """
    Px = data[:,feature_dict["Px"]]
    Pz = data[:,feature_dict["Pz"]]

    return (Px/Pz)*1000


def get_yangle(data):
    """
        This function returns a 1D array consisting of yp = Py/Pz in milliradian
    """
    Py = data[:,feature_dict["Py"]]
    Pz = data[:,feature_dict["Pz"]]

    return (Py/Pz)*1000

def get_particle_count(data, particle_name):
    return np.count_nonzero(data[:,feature_dict["PDGid"]] == particle_dict[particle_name])