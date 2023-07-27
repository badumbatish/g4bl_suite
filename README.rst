Python scripting library for plotting (and analyzing) G4Beamline program ascii output.

This library provides a soft interaction wall between G4Beamline and scientists. 

It doesn't use OOP, only functions. The function mostly manipulates 2D and 1D numpy arrays under the hood and also returns numpy arrays that can be manipulated directly by scientists.
# Installation 
```bash
pip install -i https://test.pypi.org/simple/ jjsm-fermi==0.0.3
```

# Dependencies:
    numpy==1.24.2

    mpl-scatter-density: https://github.com/astrofrog/mpl-scatter-density

    matplotlib==3.6.3
    
    tqdm==4.64.1

    
# Documentation
See https://github.com/badumbatish/fermi_proj/wiki for wiki

See https://github.com/badumbatish/fermi_proj/wiki/Automation for automation of tasks
## Basic set up

### Set your virtual detector to output ascii text format

*Before:*

> virtualdetector Det radius=15.875 length=1 color=1,1,1 material=Vacuum


*After:*
> virtualdetector Det radius=15.875 length=1 color=1,1,1 material=Vacuum **format=ascii**

### Set your output file name by placing your detector and renaming it
*Before:*
> place Det z=5921

*After*:
> place Det **rename=desired_file_name** z=5921

## Usage
```python
from g4blplot import g4blplot as plot
import matplotlib.pyplot as plt


particle_type = "pi-"

# raw data that potentially encompass multiple particles
raw_data = plot.add_text_file("desired_file_name.txt")

# get the data that is only related to pion-
data = plot.extract_particle_data(raw_data, particle_type)

# get the x position and x angle of pion-
x = plot.get_feature(data, 'x')
xp = plot.get_xangle(data)

# make a plot
pos_fig, pos_axes = plt.subplots(1, sharex=True, sharey=True, layout="constrained", subplot_kw=dict(projection="scatter_density"))

# scatter it
plot.scatter_plot(pos_axes, x, xp)
plot.save_figure(pos_fig, "position vs angle.pdf")
```
