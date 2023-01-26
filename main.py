import g4blplot as plot
import numpy as np
import matplotlib.pyplot as plt

on_data = [None]*10
off_data = [None]*10
angle = [None]*10
for i in range(0,10):
    angle[i] = (i+1)*5*0.0001
    angle_str = f"{angle[i]:.4f}".lstrip("0")
    on_data[i] = plot.add_text_file(f"on_uniform_{angle_str}_rad_detector_8.txt")
    off_data[i] = plot.add_text_file(f"off_uniform_{angle_str}_rad_detector_8.txt")

initial_pion = 100000

on_mu_count = [None]*10
off_mu_count = [None]*10
for i in range(0,10):
    on_mu_count[i] = plot.get_particle_count(on_data[i], "mu-")
    off_mu_count[i] = plot.get_particle_count(off_data[i], "mu-")


fig, axes = plt.subplots(1, layout='constrained')
angle = np.asarray(angle)

on_mu_count = (angle/0.001)**2 * on_mu_count
off_mu_count = (angle/0.001)**2 * off_mu_count

fig.suptitle("SigmaXp, sigmaYp vs normalized mu- count at detector 8")
fig.supxlabel("sigmaXp = sigmaYp")
fig.supylabel("Normalized count of mu-")

plt.scatter(angle, on_mu_count, c='b', marker="s", label='with magnets on')
plt.scatter(angle, off_mu_count, c='r', marker="o", label='with magnets off')
plt.xticks(angle)
plt.legend(loc='upper left')
plt.show()

fig.savefig("plot.pdf")
