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