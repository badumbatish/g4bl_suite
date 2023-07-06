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

def test_is_config_object():
    pass
