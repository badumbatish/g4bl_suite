import itertools
import multiprocessing as mp
import os
import subprocess
from os.path import exists
from typing import List

import matplotlib.pyplot as plt
import mpl_scatter_density
import numpy as np
import tqdm

feature_list = [
    "x",
    "y",
    "z",
    "Px",
    "Py",
    "Pz",
    "t",
    "PDGid",
    "EventID",
    "TrackID",
    "ParentID",
    "Weight",
]
feature_dict = {key: value for (value, key) in enumerate(feature_list)}

particle_dict = {"pi-": -211, "mu-": 13, "mu+": -13}


def add_text_file(file_name: str):
    """Returns a 2D numpy array that formats just like the output txt file from G4Beamline and raise exception if file does not exists

    Args:
        file_name:
            str

    Returns:
        data:
            a 2D numpy array
    """

    if exists(file_name):
        data = np.loadtxt(file_name)
    else:
        raise Exception(f"The file {file_name} does not exist")

    if len(data.shape) == 1:
        data = data[np.newaxis, :]
    return data


def scatter_plot(axes, x_axis, y_axis, heat_map: bool = False):
    """Scatter plot an axes based on 2 1D numpy array

    Args:
        axes :
            an object subplot from matplotlib that is a
        x_axis :
            1D array that denotes what to plot on the x axis
        y_axis :
            1D array that denotes what to plot on the y axis

    Returns:
        Function returns nothing, only plots a graph to the axes
    """

    if heat_map == False:
        axes.scatter(x_axis, y_axis, rasterized=False)
    else:
        density = axes.scatter_density(x_axis, y_axis)
        plt.colorbar(density, ax=axes, label="Number of points per pixel")


def hist_plot(axes, data, xlabel: str = ""):
    """
        This function plots histogram in the axes

    Args:
        axes:
            an axe plot
        data:
            a 1D numpy array

    Returns:
    A historgram plot with extra descriptive data of count, mean, std, min, 25,50,75 percentile, and max.
    ----------
    """
    axes.hist(data)
    if xlabel == "":
        axes.set_xlabel(xlabel)
        axes.set_ylabel(f"Count of {xlabel}")
    stats_str = f"Count: {data.size}\nMean: {data.mean():.3f}\nStd: {data.std():.3f}\nMin: {data.min()}\n25%: {np.percentile(data,25)}\n50%: {np.percentile(data,50)}\n75%: {np.percentile(data,75)}\nMax: {data.max()}"
    axes.text(1.01, 0.2, stats_str, transform=plt.gca().transAxes)


def set_fig_misc(fig, beam_type, plot_type):
    """Sets miscellaneous features of a figure

    Args:
        fig :

        beam_type :

        plot_type :
    Returns:
    """
    fig.suptitle((f"{beam_type.capitalize()} beam {plot_type}"))
    fig.supxlabel(f"x {plot_type}")
    fig.supylabel(f"y {plot_type}")


def save_figure(fig, file_name, dpi=300):
    """Save the figure into a file, usually pdf"""
    fig.set_size_inches((8.5, 11), forward=False)
    fig.savefig(file_name, dpi=dpi)


def extract_particle_data(data, particle_name=None, particle_id=None):
    """Extracts a numpy array of only a certain particle out of a raw data

    Args:

    Returns:
        A 2D numpy array containing only that singular particle data type

    Raises:
        An exception if there is no particle id or particle name
    """
    mask = None
    # make a 1D array mask that returns true if the PID is satisfy
    # [:,7] represents the column of PIDs
    if particle_id is not None:
        mask = data[:, feature_dict["PDGid"]] == particle_id
    elif particle_name is not None:
        mask = data[:, feature_dict["PDGid"]] == particle_dict[particle_name]
    else:
        raise Exception(f"Particle id or particle name is not present")

    # pass the mask to the raw data to select the PID-satisfying rows, then : to select all the columns of that row
    particle_data = data[mask, :]

    return particle_data


def get_feature(data, feature_name):
    """
    Returns a 1D NumPy array that is the feature in the original 2D NumPy array

    """
    return data[:, feature_dict[feature_name]]


def get_xangle(data):
    """
    This function returns a 1D array consisting of xp = Px/Pz in milliradian

    Uses numpy for its computation
    """
    Px = data[:, feature_dict["Px"]]
    Pz = data[:, feature_dict["Pz"]]

    return (Px / Pz) * 1000


def tuple_zipl(args):
    """Return a tuple of list from the argument being a list of tuples"""
    tp = []
    for v in args:
        v = list(v)
        tp.append(v)
    a = tuple(tp)
    return a


def get_yangle(data):
    """
    This function returns a 1D array consisting of yp = Py/Pz in milliradian
    """
    Py = data[:, feature_dict["Py"]]
    Pz = data[:, feature_dict["Pz"]]

    return (Py / Pz) * 1000


def get_particle_count(data, particle_name=None, particle_id=None):
    """
    Get the count of a particular particle

    """
    if particle_id is not None:
        res = np.count_nonzero(data[:, feature_dict["PDGid"]] == particle_id)
    elif particle_name is not None:
        res = np.count_nonzero(
            data[:, feature_dict["PDGid"]] == particle_dict[particle_name]
        )
    else:
        raise Exception(f"Particle id or particle name is not present")
    return res


def run_command(args):
    """
    Helper function for automate()
    """
    # print(f"Running {args}")
    result = subprocess.run(args, stdout=subprocess.DEVNULL)


def isG4BL(cmd: str) -> bool:
    """
    Check if a string representing a command ends in g4bl
    Args:
    Returns:
        boolean

    """
    return cmd.endswith("g4bl")


def isG4BLMPI(cmd: str) -> bool:
    """
    Check if a string representing a command ends in g4blmpi
    Args:
    Returns:
        boolean

    """
    return cmd.endswith("g4blmpi")


def generate_args(
    cmd: str, param_dict: dict, file_name: str, mpi_count=None
) -> List[List[str]]:
    """
    Generates a list of arguments that is the first parameter for subprocess.run


    Returns:
        List A of list B of strings, where each list B is 1 config to pass to the command line via subprocess.run
    """
    for key, value in param_dict.items():
        key = tuple(value)

    keys = []
    for element in param_dict.keys():
        if not isinstance(element, tuple):
            keys.append(element)
        else:
            keys.extend(element)

    values = []
    for element in param_dict.values():
        if not isinstance(element, tuple):
            values.append(element)
        else:
            values.append(list(v for v in element))

    combination = list(itertools.product(*param_dict.values()))

    # combination =  list(itertools.product(*values))
    def flatten(A):
        rt = []
        for i in A:
            if isinstance(i, list):
                rt.extend(flatten(i))
            else:
                rt.append(i)
        return rt

    args = []
    for each_combination in combination:
        lst = []
        lst.append(cmd)
        if isG4BLMPI(cmd):
            lst.append(str(mpi_count))
        lst.append(file_name)
        each_combination = flatten(each_combination)
        for i, value in enumerate(each_combination):
            lst.append(f"{keys[i]}={value}")
        args.append(lst)

    return args


# TODO: Return a function that takes in a configuration of unknown type, and the list of arguments, then output
# a new list of that g4bl has never computed before, in order for g4bl to not waste computation, and the physicist to not die waiting


def automate(
    cmd: str,
    param_dict: dict,
    file_name: str,
    total_process_count=1,
    mpi_count=None,
    detector_lst=None,
    data_directory=None,
):
    """
    Automating, automating, gaslighting, girlbossing, gatekeeping, mmm-kayyyy

    Automate the search space/high parameter space with G4beamline, refers to the link of Automation in the Documentation page
    Links:
        https://badumbatish.github.io/fermi_proj/automation/
    """
    args = generate_args(cmd, param_dict, file_name, str(mpi_count))

    args = skip_task_by_list(args, detector_lst, data_directory)

    process_count = 0
    if mpi_count is None:
        process_count = int(total_process_count)
    else:
        process_count = int(total_process_count / int(mpi_count))

    print(
        f"Creating pool with total process count = {total_process_count}, pool process count = {process_count}, G4BLMPI process count = {mpi_count}"
    )
    with mp.Pool(process_count) as p:
        # color is pastel pink hehe
        list(
            tqdm.tqdm(
                p.imap_unordered(run_command, args),
                total=len(args),
                colour="#F8C8DC",
                desc="Batch progress bar",
            )
        )


def filter_args(arg_lists: list) -> List[List[str]]:
    """
    Returns:
        a list of list containing string of only type "key=value"

    """
    result = []
    for lst in arg_lists:
        sub_list = []
        for item in lst:
            if "=" in item:
                sub_list.append(item)
        result.append(sub_list)

    return result


def construct_list_files(filtered_arg_list: list, postfix_string_list=None):
    """
    Constructs a list (1) of lists (2) of lists (3), where lists (3) represents the files that a batch outputs, lists (2) represents each command to the terminal.
    This function essentially constructs a list of files from the argument list generated by generate_args() and filtered via filter_args()
    Check tests/unit_test/test_remembrance.py -> test_construct_list_files()
    """
    # Constructor list file

    # if there is postfix_string_list, add to every filtered_arg_list

    # Append .txt in the end

    result = []
    for lst in filtered_arg_list:
        task_output_list = []
        std_config = ""
        for item in lst:
            std_config = std_config + item.replace("=", "")
            std_config += "|"
        std_config = std_config[: len(std_config) - 1]

        if postfix_string_list is None:
            task_output_list.append(std_config)
        else:
            for item in postfix_string_list:
                task_output_list.append(std_config + f"|{item}")
        result.append(task_output_list)
    print(result)

    def recursively_add_txt(lst: list):
        res = []
        for item in lst:
            if type(item) == list:
                res.append(recursively_add_txt(item))
            else:
                res.append(item + ".txt")
        return res

    result = recursively_add_txt(result)
    return result


def all_file_exists(data_list, data_directory=None, test=False) -> bool:
    """
    Returns:
        A boolean value that returns True if all the files in data_list, located in data_directory. It'll return false if one or more files is not present.


    """
    all_files_exist = True

    if test is True:
        relative_dir_path = "tests/unit/test_data/remembrance/"
        data_directory = os.path.join(os.getcwd(), relative_dir_path)

    for data_file in data_list:
        file_path = data_directory + data_file

        if not exists(file_path):
            print(f"File not found: {file_path}")
            all_files_exist = False

    return all_files_exist


def get_index_of_needed_tasks(data_list, data_directory=None, test=False) -> List[bool]:
    """
    Accepts a list of data files, and return a list of index that needs the tasks

    """
    res_lst = []

    for lst in data_list:
        if all_file_exists(lst, data_directory, test):
            res_lst.append(True)
        else:
            res_lst.append(False)

    return res_lst


def skip_task_by_list(
    generated_args: list, postfix_string_lst: list, data_directory=None, test=False
) -> List[List[str]]:
    """
        For a list of tasks, it returns a new list of tasks that skip over already pre-computed tasks

    Returns:
        A new list of tasks that g4beamline haven't computed
    """
    # index_list = get_index_of_needed_tasks(data_list, data_directory, test)

    new_lst = []

    filtered_arg_list = filter_args(generated_args)
    data_list = construct_list_files(
        filtered_arg_list=filtered_arg_list, postfix_string_list=postfix_string_lst
    )

    index_list = get_index_of_needed_tasks(data_list, data_directory, test)
    for index, boolean_value in enumerate(index_list):
        if boolean_value is True:
            new_lst.append(generated_args[index])

    return new_lst
