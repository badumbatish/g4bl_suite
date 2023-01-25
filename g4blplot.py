import matplotlib.pyplot as plt
import numpy as np
import mpl_scatter_density
from os.path import exists

# add feature count
feature_count = 4

# add feature name: x position, y postion and stuff
# can be used for histogram
feature_list = ["x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "TrackID", "ParentID", "Weight"]
feature_dict = {key : value for (value,key) in enumerate(feature_list)} 

particle_dict = {"pi-": -211,
                "mu-": 13}

def add_text_file(file_name):
    """Returns a 2D numpy array that formats just like the output txt file from G4Beamline and none if file does not exists

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
        return None

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

def hist_plot(axes, data):
    """
        This function plots histogram in the axes

    Parameters
    ----------
    axes :

    data :

    Returns
    ----------
    """
    for i in range(axes.size()):
        axes[i].hist(data[:,i])
        axes[i].set_xlabel(feature_list[i])

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

# returns a numpy array
# mu-, PID = 13
# pi-, PID = -211
def extract_particle_data(numpy_array, particle_name):
    """Extracts a numpy array of only a certain particle out of a raw data

    Parameters
    ----------

    Returns
    ----------
    """
    # make a 1D array mask that returns true if the PID is satisfy
    # [:,7] represents the column of PIDs
    mask = (numpy_array[:,7] == particle_dict[particle_name])

    # pass the mask to the raw data to select the PID-satisfying rows, then : to select all the columns of that row
    particle_data = numpy_array[mask,:]

    return particle_data

def get_rms_decay_angle():
    """
        This function calculates the rms decay angle from a numpy array 
        Awaiting responses and directions from Chris and Carol

    Parameters
    ----------

    Returns
    ----------
    """
    # 
    pass


def create_scatter_plot():
    """
        This function creates a tuple consists of a figure and an array of subplots that is for scatter plotting

    Parameters
    ----------

    Returns
    ----------
    """
    pass

def create_hist_plot():
    """
        This function creates a tuple consists of a figure and an array of subplots that is for histogram plotting

    Parameters
    ----------

    Returns
    ----------
    """
    pass

def get_feature(data, feature_name):
    return data[:,feature_dict[feature_name]]
    
def get_xangle(data):
    """
        This function returns a 1D array consisting of xp = Px/Pz
    """
    Px = data[:,3]
    Pz = data[:,5]

    return Px/Pz


def get_yangle(data):
    """
        This function returns a 1D array consisting of yp = Py/Pz
    """
    Py = data[:,4]
    Pz = data[:,5]

    return Py/Pz

def get_particle_count(data, particle_name):
    return np.count_nonzero(data[:,7] == particle_dict[particle_name])