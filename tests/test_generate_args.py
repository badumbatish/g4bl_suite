from g4blplot import generate_args
from g4blplot import tuple_zipl
g4bl_cmd = "g4bl"
g4blmpi_cmd = "g4blmpi"
file_name = "file_name"

def test_int_list_with_int_list():
    param_dict = {
        "_meanMomentum": [100,200,300],
        "angle": [1,2,3]
    }
    generated_args = generate_args(cmd=g4bl_cmd,param_dict=param_dict,file_name=file_name)
    test_args = [
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
    assert generated_args == test_args

def test_str_list_with_int_list():
    param_dict = {
        "_meanMomentum": ["100","200","300"],
        "angle": [1,2,3]
    }
    generated_args = generate_args(cmd=g4bl_cmd,param_dict=param_dict,file_name=file_name)
    test_args = [
        [g4bl_cmd,file_name,'_meanMomentum=100','angle=1'],
        [g4bl_cmd,file_name,'_meanMomentum=100','angle=2'],
        [g4bl_cmd,file_name,'_meanMomentum=100','angle=3'],
        [g4bl_cmd,file_name,'_meanMomentum=200','angle=1'],
        [g4bl_cmd,file_name,'_meanMomentum=200','angle=2'],
        [g4bl_cmd,file_name,'_meanMomentum=200','angle=3'],
        [g4bl_cmd,file_name,'_meanMomentum=300','angle=1'],
        [g4bl_cmd,file_name,'_meanMomentum=300','angle=2'],
        [g4bl_cmd,file_name,'_meanMomentum=300','angle=3']
    ]
    assert generated_args == test_args
def test_mixed_list_with_intfloat_list():
    param_dict = {
        "_meanMomentum": [100,"200",300],
        "angle": [1.0,2,3]
    }
    generated_args = generate_args(cmd=g4bl_cmd,param_dict=param_dict,file_name=file_name)
    test_args = [
        [g4bl_cmd,file_name,'_meanMomentum=100','angle=1.0'],
        [g4bl_cmd,file_name,'_meanMomentum=100','angle=2'],
        [g4bl_cmd,file_name,'_meanMomentum=100','angle=3'],
        [g4bl_cmd,file_name,'_meanMomentum=200','angle=1.0'],
        [g4bl_cmd,file_name,'_meanMomentum=200','angle=2'],
        [g4bl_cmd,file_name,'_meanMomentum=200','angle=3'],
        [g4bl_cmd,file_name,'_meanMomentum=300','angle=1.0'],
        [g4bl_cmd,file_name,'_meanMomentum=300','angle=2'],
        [g4bl_cmd,file_name,'_meanMomentum=300','angle=3'],
    ]
    assert generated_args == test_args


def test_list_with_tuples_of_lists():
    param_dict = {
        "_meanMomentum": [100],
        ("a","b","c"): ([4,5,6],[5,6,7])
    }
    generated_args = generate_args(cmd=g4bl_cmd,param_dict=param_dict,file_name=file_name)
    test_args = [
        [g4bl_cmd,file_name,'_meanMomentum=100','a=4','b=5','c=6'],
        [g4bl_cmd,file_name,'_meanMomentum=100','a=5','b=6','c=7']
    ]
    assert generated_args == test_args

def test_tuple_zipl():
    list1 = [4,5]
    list2 = [6,7]
    param_dict = {
        "_meanMomentum": [100],
        ("a","b") : tuple_zipl(zip(list1,list2))
    }
    generated_args = generate_args(cmd=g4bl_cmd,param_dict=param_dict,file_name=file_name)
    test_args = [
        [g4bl_cmd,file_name,'_meanMomentum=100','a=4','b=6'],
        [g4bl_cmd,file_name,'_meanMomentum=100','a=5','b=7']
    ]
    assert generated_args == test_args

def test_singular_tuple():
    param_dict = {
        "sigma": [10],
        ("Magnet","QUADgradient13", "QUADgradient2", "SOLcurrent") : (["Quadx1.5SolOFF", 0     ,0    ,0],)
    }
    generated_args = generate_args(cmd=g4bl_cmd,param_dict=param_dict,file_name=file_name)
    test_args = [
        [g4bl_cmd, file_name, 'sigma=10', 'Magnet=Quadx1.5SolOFF',"QUADgradient13=0","QUADgradient2=0","SOLcurrent=0"]
    ]
    assert generated_args == test_args