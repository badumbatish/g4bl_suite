import g4blplot as plot
import numpy as np
import matplotlib.pyplot as plt

beam_type = "negative_ellipse"
plot_type = "position"
particle_type = "mu-"
use_heat_map = False

# raw data that potentially encompass multiple particles
raw_data = plot.add_text_file(f"{beam_type}_detector_8.txt")

data = plot.extract_particle_data(raw_data, "muons-")

particle_count = np.size(data,0)
events = 100000
print(f"Particle count: {particle_count} mu- make it out of initial {events} pions-")

"""set_fig_misc(gaussian_position_fig, beam_type=beam_type, plot_type=plot_type)
scatter_plot(gaussian_position_axes, data[0], heat_map=use_heat_map)
# gaussian_position_axes.set_title("Detector 1 (4mm away from beam source")
save_figure(gaussian_position_fig, f"pics/{beam_type}_position.pdf")

plot_type = "momentum"
gaussian_momentum_fig, gaussian_momentum_axes = plt.subplots(1, sharex=True, sharey=True, layout="constrained", subplot_kw=dict(projection="scatter_density"))
set_fig_misc(gaussian_position_fig, beam_type=beam_type, plot_type=plot_type)

scatter_plot(gaussian_momentum_axes, data[0], plot_type=plot_type, heat_map=use_heat_map)
# gaussian_momentum_axes.set_title("Detector 1 (4mm away from beam source")
save_figure(gaussian_momentum_fig,  f"pics/{beam_type}_momentum.pdf")


gaussian_hist_fig, gaussian_hist_axes = plt.subplots(feature_count, sharey=True, layout="constrained")
gaussian_hist_fig.supylabel("count")
hist_plot(gaussian_hist_axes, data[0])
save_figure(gaussian_hist_fig,f"pics/{beam_type}_hist.pdf")"""