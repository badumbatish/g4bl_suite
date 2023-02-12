import g4blplot as plot
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    fig, axes = plt.subplots(1, layout='constrained')

    fig.suptitle("SigmaXp, sigmaYp vs normalized mu- count at end of beamline (50mm rad detector)")
    fig.supxlabel("uniform sigmaXp = sigmaYp")
    fig.supylabel("Normalized count of mu-")
    
    initial_pion = 10000000
    num = 40
    angle = [None]*num
    starting_angle = 0
    divider = initial_pion/100000
    for i in range(0, num):
        angle[i] = f"{starting_angle+(i+1)*5*0.0001:.4f}"
    print(angle)

    file_name = "Pion_Line_BeamEllipse.g4bl"
    multiplier = 1.5 
    command = "/home/jjsm/G4beamline-3.08-source/build/bin/g4blmpi"
    param_dict = {
        "_meanMomentum": [150,100],
        "nEv" : [initial_pion],
        "_sigmaXY": [-5],
        "_sigmaXYp": angle,
        ("Magnet","QUADgradient13", "QUADgradient2", "SOLcurrent") : (["ON", f"{0.140*multiplier:.4f}", f"{-0.155*multiplier:.4f}",f"{158.2*multiplier:.4f}"],
                                                                    ["OFF", 0,0,0])
    }
    plot.automate(command,param_dict,file_name,total_process_count=12,mpi_count=6)
    beam = [None] * num * 4

    for i in range(0,num):
        beam[i] = plot.add_text_file(f"MeV150|nEv{initial_pion}|MagnetON|angle{angle[i]}|detector_8.txt")
        beam[i+num*1] = plot.add_text_file(f"MeV150|nEv{initial_pion}|MagnetOFF|angle{angle[i]}|detector_8.txt")
        beam[i+num*2] = plot.add_text_file(f"MeV100|nEv{initial_pion}|MagnetON|angle{angle[i]}|detector_8.txt")
        beam[i+num*3] = plot.add_text_file(f"MeV100|nEv{initial_pion}|MagnetOFF|angle{angle[i]}|detector_8.txt")

    mu_count = [None] * num * 4
    for pt in range(0,4):
        for i in range(0,num):
            mu_count[i+num*pt] = plot.get_particle_count(beam[i+num*pt],"mu-")
 

    mu_count = np.asarray(mu_count)
    angle = np.array(angle,dtype=float)
    for pt in range(0,4):
        for i in range(0,num):
            mu_count[i+num*pt] = (angle[i]/0.001)**2 * mu_count[i+num*pt] / divider
            
    label = ['150MeV with magnets on','150MeV with magnets off','100MeV with magnets on', '100MeV with magnets off']
    c = ['b','b', 'r', 'r']
    marker = ['s','o','s','o']
    for pt in range(0,4):
        plt.scatter(angle, mu_count[num*pt:num*(pt+1)],c=c[pt], marker= marker[pt], label=label[pt])
    
    plt.legend(loc='upper left')
    plt.show()

    plot.save_figure(fig,"plot.pdf")

