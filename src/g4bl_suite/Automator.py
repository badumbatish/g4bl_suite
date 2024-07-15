from __future__ import annotations

import itertools
import multiprocessing as mp
import os
import subprocess
from os.path import exists
from typing import List
import tqdm


class Automator:
    def __init__(self):
        self.cmd = None
        self.file_name = None
        self.params_dict = None

    def set_cmd(self, cmd) -> Automator:
        self.cmd = cmd
        return self

    def set_params_dict(self, params_dict) -> Automator:
        self.params_dict = params_dict
        return self

    def set_file_name(self, file_name) -> Automator:
        self.file_name = file_name
        return self

    def is_g4bl(self) -> bool:
        """
        Check if a string representing a command ends in g4bl
        Args:
        Returns:
            boolean

        """

        return self.cmd.endswith("g4bl")

    def is_g4bl_mpi(self) -> bool:
        """
        Check if a string representing a command ends in g4blmpi
        Args:
        Returns:
            boolean

        """
        return self.cmd.endswith("g4blmpi")

    def generate_args(self, mpi_count=None) -> List[List[str]]:
        """
        Generates a list of arguments that is the first parameter for subprocess.run


        Returns:
            List A of list B of strings, where each list B is 1 config to pass to the command line via subprocess.run
        """

        keys = []
        values = []
        for key, value in self.params_dict.items():
            # Handle keys: Extend with elements if key is a tuple
            # or add the key itself in form of a list if it's not a tuple
            keys.extend(key if isinstance(key, tuple) else [key])

            # Handle values: Append the value converted into a list if it's a tuple, otherwise append the value itself
            values.append(list(value) if isinstance(value, tuple) else value)

        # combinations = list(itertools.product(*param_dict.values()))

        combinations = list(itertools.product(*values))

        def flatten(a):
            rt = []
            for x in a:
                if isinstance(x, list):
                    rt.extend(flatten(x))
                else:
                    rt.append(x)
            return rt

        args = []
        for combination in combinations:
            lst = [self.cmd]
            if self.is_g4bl_mpi():
                lst.append(str(mpi_count))
            lst.append(self.file_name)
            combination = flatten(combination)
            for i, value in enumerate(combination):
                lst.append(f"{keys[i]}={value}")
            args.append(lst)

        return args

    def tuple_zipl(self, args):
        """Return a tuple of list from the argument being a list of tuples"""
        tp = []
        for v in args:
            v = list(v)
            tp.append(v)
        a = tuple(tp)
        return a

    def run_command(self, args):
        """
        Helper function for automate()
        """
        # print(f"Running {args}")
        subprocess.run(args, stdout=subprocess.DEVNULL)

    # TODO: Return a function that takes in a configuration of unknown type, and the list of arguments, then output
    # a new list of that g4bl has never computed before,
    # in order for g4bl to not waste computation, and the physicist to not die waiting

    def automate(
        self,
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
        args = self.generate_args(str(mpi_count))

        if not (data_directory is None):
            args = self.skip_task_by_list(args, detector_lst, data_directory)

        if mpi_count is None:
            process_count = int(total_process_count)
        else:
            process_count = int(total_process_count / int(mpi_count))

        print(
            f"Creating pool with total process count = {total_process_count},"
            f"pool process count = {"
                "process_count}, G4BLMPI process count = {mpi_count}"
        )
        with mp.Pool(process_count) as p:
            # color is pastel pink hehe
            list(
                tqdm.tqdm(
                    p.imap_unordered(self.run_command, args),
                    total=len(args),
                    colour="#F8C8DC",
                    desc="Batch progress bar",
                )
            )

    def filter_args(self, arg_lists: List[List[str]]) -> List[List[str]]:
        """
        Filters each sublist in the input list of lists, returning only those strings
        that follow the 'key=value' format.

        Args:
            arg_lists (List[List[str]]): A list of lists, where each sublist contains strings.

        Returns:
            List[List[str]]: A list of sublists containing strings formatted as 'key=value'.

        Examples:
        >>> Automator().filter_args([["name=John", "age=30"], ["error", "size=medium"]])
        [['name=John', 'age=30'], ['size=medium']]

        >>> Automator().filter_args([["valid=100", "invalid"], [], ["key=value", "setting"]])
        [['valid=100'], ['key=value']]

        >>> Automator().filter_args([["123", "check=ok"], ["test=", "=data"]])
        [['check=ok']]
        """
        result = []
        for lst in arg_lists:
            sub_list = [item for item in lst if 0 <
                        item.find("=") < len(item) - 1]
            if len(sub_list) != 0:
                result.append(sub_list)

        return result

    def construct_list_files(self, filtered_arg_list: list, postfix_string_list=None):
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

        def recursively_add_txt(items: list):
            res = []
            for temp_item in items:
                if isinstance(temp_item, list):
                    # Recurse if the item is a list
                    res.append(recursively_add_txt(temp_item))
                else:
                    res.append(f"{temp_item}.txt")
            return res

        result = recursively_add_txt(result)
        return result

    def all_file_exists(self, data_list, data_directory=None, test=False) -> bool:
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

    def get_index_of_needed_tasks(
        self, data_list, data_directory=None, test=False
    ) -> List[bool]:
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
        return [
            bool(self.all_file_exists(file, data_directory, test)) for file in data_list
        ]

    def skip_task_by_list(
        self,
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
        filtered_args = self.filter_args(tasks)
        task_files = self.construct_list_files(filtered_args, postfixes)
        needed_task_indices = self.get_index_of_needed_tasks(
            task_files, data_directory, test
        )

        # Select and return tasks that have not been completed yet
        return [tasks[i] for i, needed in enumerate(needed_task_indices) if needed]
