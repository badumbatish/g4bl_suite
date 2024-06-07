import matplotlib.pyplot as plt
import numpy as np

from g4bl_suite import g4blplot as plot

if __name__ == "__main__":
    initial_pion = 100
    num = 13
    angle = [None] * num
    starting_angle = 0.002
    divider = initial_pion / 100000
    for i in range(0, num):
        angle[i] = f"{starting_angle+(i)*0.004:.4f}"
    print(angle)

    file_name = "Pion_Line_BeamEllipse.g4bl"
    quad_multiplier = 1.5
    multiplier = 1.5
    command = "/home/jjsm/G4beamline-3.08-source/build/bin/g4bl"
    param_dict = {
        "_meanMomentum": [100],
        "nEv": [initial_pion],
        "_sigmaXY": [-5],
        "_sigmaXYp": angle,
        ("Magnet", "QUADgradient13", "QUADgradient2", "SOLcurrent"): (
            [
                "Quadx1.5SolOFF",
                f"{0.140*quad_multiplier:.4f}",
                f"{-0.155*quad_multiplier:.4f}",
                f"{158.2*0:.4f}",
            ],
            [
                "Quadx1.5SolNOR",
                f"{0.140*quad_multiplier:.4f}",
                f"{-0.155*quad_multiplier:.4f}",
                f"{158.2*1:.4f}",
            ],
            [
                "Quadx1.5Solx1.5",
                f"{0.140*quad_multiplier:.4f}",
                f"{-0.155*quad_multiplier:.4f}",
                f"{158.2*1.5:.4f}",
            ],
            [
                "Quadx1.5Solx2.0",
                f"{0.140*quad_multiplier:.4f}",
                f"{-0.155*quad_multiplier:.4f}",
                f"{158.2*2:.4f}",
            ],
            [
                "Quadx.15Solx2.5",
                f"{0.140*quad_multiplier:.4f}",
                f"{-0.155*quad_multiplier:.4f}",
                f"{158.2*2.5:.4f}",
            ],
        ),
    }

    plot.automate(
        command, param_dict, file_name, total_process_count=10, mpi_count=None
    )

    """
    magType = ["QuadNORSolOFF",
                "QuadNORSolNOR",
                "QuadNORSolx1.5",
                 "QuadNORSolx2.0",
                  "QuadNORSolx2.5",
                  "Quadx1.5SolOFF",
                  "Quadx1.5SolNOR",
                  "Quadx1.5Solx1.5",
                  "Quadx1.5Solx2.0",
                  "Quadx.15Solx2.5"]

    pt = len(magType)
    
    beam = [[None for i in range (0, num)] for j in range (0, pt) ] 
    print(len(magType))
    print(len(angle))

    data_dir = "../../data/normalQuad_versus_solenoid"
    for m in range(0, pt):
        for n in range(0,num):
            print(f"Adding MeV100|nEv{initial_pion}|Magnet{magType[m]}|angle{angle[n]}|detector_8.txt")
            beam[m][n] = plot.add_text_file(f"{data_dir}/MeV100|nEv{initial_pion}|Magnet{magType[m]}|angle{angle[n]}|detector_8.txt")

    mu_count = [[None for i in range (0, num)] for j in range (0, pt) ] 
    for m in range(0, pt):
        for n in range(0,num):
            mu_count[m][n] = plot.get_particle_count(beam[m][n],"mu-")
        print (mu_count[m])
            
 
    numbers_set = set(i for j in mu_count for i in j)
    print(len(numbers_set)) # 10
    
    mu_count = np.asarray(mu_count)
    angle = np.array(angle,dtype=float)

    for m in range(0, pt):
        for n in range(0,num):
            mu_count[m][n] = (angle[n]/0.001)**2 * mu_count[m][n] / divider
    print(mu_count.size)      


    fig, axes = plt.subplots(1, layout='constrained')

    fig.suptitle("100MeV: SigmaXp, sigmaYp vs unnormalized mu- count at end of beamline (50mm rad detector)")
    fig.supxlabel("uniform sigmaXp = sigmaYp")
    fig.supylabel("Unnormalized count of mu-")

    label = ['Nominal Quad, Solenoid Off',
            'Nominal Quad, Nominal Solenoid',
            'Nominal Quad, Solenoid x1.5',
             'Nominal Quad, Solenoid x2.0',
              'Nominal Quad, Solenoid x2.5',
              'Quad x1.5, Solenoid Off',
              'Quad x1.5, Nominal Solenoid',
              'Quad x1.5, Solenoid x1.5',
              'Quad x1.5, Solenoid x2.0',
              'Quad x1.5, Solenoid x2.5']
    
    color = iter(plt.cm.tab20(np.linspace(0, 1, n)))

    #marker = ['s','o','s','o']
    for m in range(0,pt):
        c = next(color)
        axes.scatter(angle, mu_count[m],c=c, label=label[m])
    axes.legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left",
                mode="expand", borderaxespad=0, ncols=3, handletextpad=0.01, columnspacing=0.8)
    #plt.legend(loc='upper left')
    fig.set_size_inches((8.5, 11), forward=False)
    fig.savefig("normalized.pdf", bbox_inches="tight")
    plt.show()
    """
