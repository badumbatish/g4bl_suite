import matplotlib.pyplot as plt
import numpy as np
from os.path import exists

def add_file():
    data = [None] * 8

    for i in range(0, 8):
        ascii_output_file =  "detector" + str(i+1) + ".txt"
        if(exists(ascii_output_file)):
            data[i] = np.loadtxt(ascii_output_file)
    return data

data = add_file()

def fig_plot(fig, axes, data, plot_type = "position"):
    fig.suptitle("Gaussian beam " + plot_type + " graph", fontsize="16")
    fig.supxlabel("x " + plot_type)
    fig.supylabel("y " + plot_type)
    plot(axes[0], data[0], plot_type)
    axes[0].set_title(f"Detector 1 (4mm away from beam source)")

    plot(axes[1], data[7], plot_type)
    axes[1].set_title(f"Detector 8 (5915mm away from beam source)")


def plot(axes,data,plot_type = "position"):
    # The second input of data[] is the column
    # 0: x position
    # 1: y position
    # 2: Xp position
    # 3: Yp position
    if plot_type == "position" :
        x = data[:,0]
        y= data[:,1]
        axes.scatter(x,y)
    elif plot_type == "momentum" :
        x = data[:,2]
        y = data[:,3]
        axes.scatter(x,y)

fig1, axes1 = plt.subplots(2, sharex=True, sharey=True)
fig_plot(fig1, axes1, data, "position")
plt.savefig('pics/gaussian_position_report.png', dpi=1200)

fig2, axes2 = plt.subplots(2, sharex=True, sharey=True)
fig_plot(fig2, axes2, data, "momentum")
plt.savefig('pics/gaussian_momentum_report.png', dpi=1200)
plt.show()