import g4blplot as plot
import numpy as np
import matplotlib.pyplot as plt

data = [None]*10
angle = [None]*10
for i in range(0,10):
    angle[i] = (i+1)*5
    data[i] = plot.add_text_file(f"data/uniform_.00{angle[i]:02d}_rad_detector_8.txt")

initial_pion = 100000

mu_count = [None]*10
for i in range(0,10):
    mu_count[i] = plot.get_particle_count(data[i], "mu-")


fig, axes = plt.subplots(1, layout='constrained')
angle = np.asarray(angle)*0.0001
mu_count = np.asarray(mu_count)
axes.set_xlabel("sigmaXp = sigmaYp")
axes.set_ylabel("Count of mu- (out of 100000 initial pi-)")
axes.set_xticks(angle)
axes.set_title("With magnets and solenoid turned off")
plt.scatter(angle, mu_count)

plt.show()

fig.savefig("plot.pdf")
