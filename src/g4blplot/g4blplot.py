import doctest
import itertools
import multiprocessing as mp
import os
import subprocess
from os.path import exists
from typing import List

import matplotlib.pyplot as plt
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


def add_text_file(file_name: str, **kwargs):
    """Returns a 2D numpy array that formats just like
        the output txt file from G4Beamline and raise exception if file does not exist

    Args:
        file_name:
            str

    Returns:
        data:
            a 2D numpy array
    """

    if exists(file_name):
        data = np.genfromtxt(fname=file_name, **kwargs)
    else:
        raise Exception(f"The file {file_name} does not exist")

    if len(data.shape) == 1:
        data = data[np.newaxis, :]
    return data


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


def extract_particle_data(data, particle_name=None, particle_id=None):
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


def get_x_angle(data):
    """
    This function returns a 1D array consisting of xp = Px/Pz in milliradian

    Uses numpy for its computation
    """
    p_x = data[:, feature_dict["Px"]]
    p_z = data[:, feature_dict["Pz"]]

    return (p_x / p_z) * 1000


def tuple_zipl(args):
    """Return a tuple of list from the argument being a list of tuples"""
    tp = []
    for v in args:
        v = list(v)
        tp.append(v)
    a = tuple(tp)
    return a


def get_y_angle(data):
    """
    This function returns a 1D array consisting of yp = Py/Pz in milliradian
    """
    p_y = data[:, feature_dict["Py"]]
    p_z = data[:, feature_dict["Pz"]]

    return (p_y / p_z) * 1000


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
    subprocess.run(args, stdout=subprocess.DEVNULL)


def is_g4bl(cmd: str) -> bool:
    """
    Check if a string representing a command ends in g4bl
    Args:
    Returns:
        boolean

    """
    return cmd.endswith("g4bl")


def is_g4bl_mpi(cmd: str) -> bool:
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
    def flatten(a):
        rt = []
        for x in a:
            if isinstance(x, list):
                rt.extend(flatten(x))
            else:
                rt.append(x)
        return rt

    args = []
    for each_combination in combination:
        lst = [cmd]
        if is_g4bl_mpi(cmd):
            lst.append(str(mpi_count))
        lst.append(file_name)
        each_combination = flatten(each_combination)
        for i, value in enumerate(each_combination):
            lst.append(f"{keys[i]}={value}")
        args.append(lst)

    return args


# TODO: Return a function that takes in a configuration of unknown type, and the list of arguments, then output
# a new list of that g4bl has never computed before,
# in order for g4bl to not waste computation, and the physicist to not die waiting


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

    Automate the search space/high parameter space with G4Beamline,
    refers to the link of Automation in the Documentation page
    Links:
        https://badumbatish.github.io/fermi_proj/automation/
    """
    args = generate_args(cmd, param_dict, file_name, str(mpi_count))

    if not (data_directory is None):
        args = skip_task_by_list(args, detector_lst, data_directory)

    if mpi_count is None:
        process_count = int(total_process_count)
    else:
        process_count = int(total_process_count / int(mpi_count))

    print(
        f"Creating pool with total process count = {total_process_count},"
        f"pool process count = {process_count}, G4BLMPI process count = {mpi_count}"
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


def filter_args(arg_lists: List[List[str]]) -> List[List[str]]:
    """
    Filters each sublist in the input list of lists, returning only those strings
    that follow the 'key=value' format.

    Args:
        arg_lists (List[List[str]]): A list of lists, where each sublist contains strings.

    Returns:
        List[List[str]]: A list of sublists containing strings formatted as 'key=value'.

    Examples:
    >>> filter_args([["name=John", "age=30"], ["error", "size=medium"]])
    [['name=John', 'age=30'], ['size=medium']]
    >>> filter_args([["valid=100", "invalid"], [], ["key=value", "setting"]])
    [['valid=100'], ['key=value']]
    >>> filter_args([["123", "check=ok"], ["test=", "=data"]])
    [['check=ok']]
    """
    result = []
    for lst in arg_lists:
        sub_list = [item for item in lst if 0 < item.find("=") < len(item) - 1]
        if len(sub_list) != 0:
            result.append(sub_list)

    return result


def construct_list_files(filtered_arg_list: list, postfix_string_list=None):
    """
    Constructs a list (1) of lists (2) of lists (3), where lists (3) represents the files
        that a batch outputs, lists (2) represents each command to the terminal.
    This function essentially constructs a list of files from the argument list generated by generate_args()
        and filtered via filter_args()
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

    def recursively_add_txt(temp_lst: list):
        res = []
        for temp_item in temp_lst:
            if isinstance(temp_item, list):
                res.append(recursively_add_txt(temp_item))
            else:
                res.append(temp_item + ".txt")
        return res

    result = recursively_add_txt(result)
    return result


def all_file_exists(data_list, data_directory=None, test=False) -> bool:
    """
    Returns:
        A boolean value that returns True if all the files in data_list,
         located in data_directory. It'll return false if one or more files is not present.


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
    Determines which tasks need to be executed based on the existence of their associated data files.

    Args:
        data_list (List[str]): List of data file names or paths associated with tasks.
        data_directory (str, optional): Directory to prepend to file names for existence checks. Defaults to None.
        test (bool, optional): Indicates whether this function is being called in a test environment. Defaults to False.

    Returns:
        List[bool]: A list where each element is a boolean indicating
        whether the task associated with the corresponding index in `data_files` needs to be executed
        (True if it does not exist and False otherwise).
    """
    # Determine the existence of each file
    # and return the negation (True if file does not exist and hence task is needed)
    return [bool(all_file_exists(file, data_directory, test)) for file in data_list]


def skip_task_by_list(
    tasks: List[List[str]],
    postfixes: List[str],
    data_directory: str = None,
    test: bool = False,
) -> List[List[str]]:
    """
    Filters out tasks that have already been computed and returns a list of tasks still needing processing.

    Args:
        tasks (List[str]): List of task identifiers.
        postfixes (List[str]): List of postfix strings used to check task completion.
        data_directory (str, optional): Directory where task outputs are stored. Defaults to None.
        test (bool, optional): Flag for test mode. Defaults to False.

    Returns:
        List[str]: List of tasks that have not yet been computed.
    """
    filtered_args = filter_args(tasks)
    task_files = construct_list_files(filtered_args, postfixes)
    needed_task_indices = get_index_of_needed_tasks(task_files, data_directory, test)

    # Select and return tasks that have not been completed yet
    return [tasks[i] for i, needed in enumerate(needed_task_indices) if needed]


if __name__ == "__main__":
    doctest.testmod()
