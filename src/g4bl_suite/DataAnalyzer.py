from os.path import exists

import numpy as np
import matplotlib.pyplot as plt
from g4bl_suite.GlobalVariables import feature_dict, particle_dict


class DataAnalyzer:
    def __init__(self, file_name: str, **kwargs):
        """Constructs a 2D numpy array that formats just like
        the output txt file from G4Beamline and raise exception if file does not exist

        Args:
            file_name:
                str

        Returns:
            data:
                a 2D numpy array
        """
        if exists(file_name):
            self.data = np.genfromtxt(fname=file_name, **kwargs)
        else:
            raise Exception(f"The file {file_name} does not exist")

        if len(self.data.shape) == 1:
            self.data = self.data[np.newaxis, :]

    def extract_particle_data(self, particle_name=None, particle_id=None):
        """Extracts a numpy array of only a certain particle out of a raw data

        Args:

        Returns:
            A 2D numpy array containing only that singular particle data type

        Raises:
            An exception if there is no particle id or particle name
        """
        # make a 1D array mask that returns true if the PID is satisfied
        # [:,7] represents the column of PIDs
        if particle_id is not None:
            mask = self.data[:, feature_dict["PDGid"]] == particle_id
        elif particle_name is not None:
            mask = self.data[:, feature_dict["PDGid"]] == particle_dict[particle_name]
        else:
            raise Exception(f"Particle id or particle name is not present")

        # pass the mask to the raw data to select the PID-satisfying rows, then : to select all the columns of that row
        particle_data = self.data[mask, :]

        return particle_data

    def get_feature(self, feature_name):
        """
        Returns a 1D NumPy array that is the feature in the original 2D NumPy array

        """
        return self.data[:, feature_dict[feature_name]]

    def get_x_angle(self):
        """
        This function returns a 1D array consisting of xp = Px/Pz in milliradian

        Uses numpy for its computation
        """
        p_x = self.data[:, feature_dict["Px"]]
        p_z = self.data[:, feature_dict["Pz"]]

        return (p_x / p_z) * 1000

    def get_y_angle(self):
        """
        This function returns a 1D array consisting of yp = Py/Pz in milliradian
        """
        p_y = self.data[:, feature_dict["Py"]]
        p_z = self.data[:, feature_dict["Pz"]]

        return (p_y / p_z) * 1000

    def get_particle_count(self, particle_name=None, particle_id=None):
        """
        Get the count of a particular particle

        """
        if particle_id is not None:
            res = np.count_nonzero(self.data[:, feature_dict["PDGid"]] == particle_id)
        elif particle_name is not None:
            res = np.count_nonzero(
                self.data[:, feature_dict["PDGid"]] == particle_dict[particle_name]
            )
        else:
            raise Exception(f"Particle id or particle name is not present")
        return res


def scatter_plot(axes, x_axis, y_axis, heat_map: bool = False):
    """Scatter plot an axes based on 2 1D numpy array

    Args:
        axes :
            an object subplot from matplotlib that is an
        x_axis :
            1D array that denotes what to plot on the x-axis
        y_axis :
            1D array that denotes what to plot on the y-axis
        heat_map :
            A boolean, True if you want to use heat map, defaults to False

    Returns:
        Function returns nothing, only plots a graph to the axes
    """

    if not heat_map:
        axes.scatter(x_axis, y_axis, rasterized=False)
    else:
        density = axes.scatter_density(x_axis, y_axis)
        plt.colorbar(density, ax=axes, label="Number of points per pixel")


def hist_plot(axes, data, x_label: str = ""):
    """
        This function plots histogram in the axes

    Args:
        axes:
            an axe plot
        data:
            a 1D numpy array
        x_label:
            a string for x-label of the histogram plot

    Returns:
        A histogram plot with extra descriptive data of count, mean, std, min, 25,50,75 percentile, and max.
    ----------
    """
    axes.hist(data)
    if x_label == "":
        axes.set_xlabel(x_label)
        axes.set_ylabel(f"Count of {x_label}")
    stats_str = (
        f"Count: {data.size}\nMean: {data.mean():.3f}\nStd: "
        f"{data.std():.3f}\nMin: {data.min()}\n"
        f"25%: {np.percentile(data, 25)}\n50%: {np.percentile(data, 50)}\n"
        f"75%: {np.percentile(data, 75)}\nMax: {data.max()}"
    )
    axes.text(1.01, 0.2, stats_str, transform=plt.gca().transAxes)


def set_fig_misc(fig, beam_type, plot_type):
    """Sets miscellaneous features of a figure

    Args:
        fig :

        beam_type :

        plot_type :
    Returns:
    """
    fig.suptitle(f"{beam_type.capitalize()} beam {plot_type}")
    fig.supxlabel(f"x {plot_type}")
    fig.supylabel(f"y {plot_type}")


def save_figure(fig, file_name, dpi=300):
    """Save the figure into a file, usually pdf"""
    fig.set_size_inches((8.5, 11), forward=False)
    fig.savefig(file_name, dpi=dpi)
