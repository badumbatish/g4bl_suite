from g4blplot import g4blplot

import os
from os.path import exists
import glob
from pathlib import Path

path = os.path.dirname(os.path.realpath(__file__))  # directory path of the app


g4bl_cmd = "g4bl"
g4blmpi_cmd = "g4blmpi"

file_name = "file_name"





def test_is_file_exists():
    assert exists(os.path.join(path, "test_data/dummy_file.txt")) == True

def test_extract_from_args():

    param_dict = {
        "_meanMomentum": ["100","200","300"],
        "angle": [1,2,3]
    }
    generated_args = g4blplot.generate_args(cmd=g4bl_cmd,param_dict=param_dict,file_name=file_name)
    """
    The generated arguments will look like this 
    generator_args = [
        [g4bl_cmd,file_name,'_meanMomentum=100','angle=1'],
        [g4bl_cmd,file_name,'_meanMomentum=100','angle=2'],
        [g4bl_cmd,file_name,'_meanMomentum=100','angle=3'],
        [g4bl_cmd,file_name,'_meanMomentum=200','angle=1'],
        [g4bl_cmd,file_name,'_meanMomentum=200','angle=2'],
        [g4bl_cmd,file_name,'_meanMomentum=200','angle=3'],
        [g4bl_cmd,file_name,'_meanMomentum=300','angle=1'],
        [g4bl_cmd,file_name,'_meanMomentum=300','angle=2'],
        [g4bl_cmd,file_name,'_meanMomentum=300','angle=3'],
    ]
    """
    test_args = [ 
       [ '_meanMomentum=100','angle=1'],
       [ '_meanMomentum=100','angle=2'],
       [ '_meanMomentum=100','angle=3'],
       [ '_meanMomentum=200','angle=1'],
       [ '_meanMomentum=200','angle=2'],
       [ '_meanMomentum=200','angle=3'],
       [ '_meanMomentum=300','angle=1'],
       [ '_meanMomentum=300','angle=2'],
       [ '_meanMomentum=300','angle=3'],
     ]
    assert g4blplot.filter_args(generated_args) == test_args

def test_construct_list_files():
    postfix_string_list = [ "detector1",
                            "detector2",
                          ]
    filtered_arg_list = [
       [ '_meanMomentum=100','angle=1'],
       [ '_meanMomentum=100','angle=2'],
       [ '_meanMomentum=100','angle=3'],
       [ '_meanMomentum=200','angle=1'],
       [ '_meanMomentum=200','angle=2'],
       [ '_meanMomentum=200','angle=3'],
       [ '_meanMomentum=300','angle=1'],
       [ '_meanMomentum=300','angle=2'],
       [ '_meanMomentum=300','angle=3'],
    ]
    
    test_args = [
            [
                '_meanMomentum100|angle1|detector1.txt',
                '_meanMomentum100|angle1|detector2.txt',
            ],
            [
                '_meanMomentum100|angle2|detector1.txt',
                '_meanMomentum100|angle2|detector2.txt',
            ],
            [
                
                '_meanMomentum100|angle3|detector1.txt',
                '_meanMomentum100|angle3|detector2.txt',
            ],
            [
                
                '_meanMomentum200|angle1|detector1.txt',
                '_meanMomentum200|angle1|detector2.txt',
            ],
            [
                
                '_meanMomentum200|angle2|detector1.txt',
                '_meanMomentum200|angle2|detector2.txt',
            ],
            [
                
                '_meanMomentum200|angle3|detector1.txt',
                '_meanMomentum200|angle3|detector2.txt',
            ],
            [
                
                '_meanMomentum300|angle1|detector1.txt',
                '_meanMomentum300|angle1|detector2.txt',
            ],
            [
                
                '_meanMomentum300|angle2|detector1.txt',
                '_meanMomentum300|angle2|detector2.txt',
            ],
            [
                
                '_meanMomentum300|angle3|detector1.txt',
                '_meanMomentum300|angle3|detector2.txt',
            ],
    ]
    assert g4blplot.construct_list_files(filtered_arg_list=filtered_arg_list,
                                         postfix_string_list = postfix_string_list) == test_args

def test_all_file_exists():

    # All file exists
    all_lst = [
                '_meanMomentum100|angle1|detector1.txt',
                '_meanMomentum100|angle1|detector2.txt',
                ]
    assert g4blplot.all_file_exists(all_lst, data_directory= None, test = True) == True


    # Half of list of file exists, should return False
    half_lst = [
                
                '_meanMomentum200|angle1|detector1.txt',
                '_meanMomentum200|angle1|detector2.txt',
            ]

    assert g4blplot.all_file_exists(half_lst, data_directory= None, test = True) == False



def test_get_index_of_needed_tasks():
    """
        Test the function to see if it is truly getting the index of the needed tasks, not the already computed tasks

        if the task lists that automate() has 4 tasks, and task 0th and task 3rd can be skipped, it should return an object that contains only
        index 1 and 2, or if
            - the function is returning a list, then it should return all a list of 4 elements, where 1st and 2nd element is true, 0th and 4th is false
            - the function is returning a set, then it should return a set of all needed integers only
    """
    postfix_string_list = [ "detector1",
                            "detector2",
                          ]
    filtered_arg_list = [
       [ '_meanMomentum=100','angle=1'],
       [ '_meanMomentum=100','angle=2'],
       [ '_meanMomentum=100','angle=3'],
       [ '_meanMomentum=200','angle=1'],
       [ '_meanMomentum=200','angle=2'],
       [ '_meanMomentum=200','angle=3'],
       [ '_meanMomentum=300','angle=1'],
       [ '_meanMomentum=300','angle=2'],
       [ '_meanMomentum=300','angle=3'],
    ]

    data_list_of_list =  g4blplot.construct_list_files(filtered_arg_list=filtered_arg_list,
                                         postfix_string_list = postfix_string_list)

    result_list = []

    # First 3 element is True, middle 5 element is False, last element is True
    for _ in range(3):
        result_list.append(True)
    for _ in range(5):
        result_list.append(False)
    for _ in range(1):
        result_list.append(True)
    
    assert True
    assert g4blplot.get_index_of_needed_tasks(data_list = data_list_of_list, data_directory = None, test = True) == result_list
