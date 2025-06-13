import os
from datetime import datetime
import reading
import analyzing
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import simpson
import imageio
from glob import glob
import re

def chosen_variable_settings(chosen_variable):
    variable_settings = {
        0 : ['thickness', 'd', 'A'],
        1 : ['Irradiation', 'irr', 'eV']
    }
    return variable_settings.get(chosen_variable, f'There are no settings for {chosen_variable} as chosen variable.' )

def plot_and_save_outer_spectrum_and_yield(analyzed_data, time_to_read, chosen_variable, save_folder):
    print('Making plots and saving data of outer spectra and yields...')
    # material, variable, energy, spectrum, 
    data_to_plot = []
    for i in range(len(analyzed_data)):

        analyzed_folder = analyzed_data[i][1]
        material = reading.read_material(analyzed_data[i][0])
        variable = reading.variable_read(chosen_variable, analyzed_data[i][0])
        
        index_time_to_read = next((i for i, item in enumerate(analyzed_folder) if item[0] == read_spectrum(time_to_read, analyzed_folder)), -1)
        energy = analyzed_folder[index_time_to_read][2]
        spectrum = analyzed_folder[index_time_to_read][3]
        time = analyzed_folder[index_time_to_read][0]
        e_yield = analyzed_folder[index_time_to_read][1]
        
        data_to_plot.append((material, variable, time, e_yield, energy, spectrum))
    
    data_to_plot = sorted(data_to_plot, key = lambda x: (x[0], x[1]))

    # PLOT OUTER ELECTRON SPECTRUM
    for i in range(len(data_to_plot)):
        material = data_to_plot[i][0]
        variable = data_to_plot[i][1]
        time = data_to_plot[i][2]
        energy = data_to_plot[i][4]
        for j in range(len(energy)):
            energy[j] = energy[j] - analyzing.work_function_library(material)
        spectrum = data_to_plot[i][5]
        my_label = chosen_variable_settings(chosen_variable)[1] + f'({material}, {round(time, 1)} fs) = {variable} ' + chosen_variable_settings(chosen_variable)[2]
        plt.plot(energy, spectrum, linestyle = '-', label = my_label)

        # save the data
        with open(os.path.join(save_folder, f'spectrum_{material}_{chosen_variable_settings(chosen_variable)[1]}={variable}.txt'), 'w') as file:
            for x, y in zip(energy, spectrum):
                file.write(f'{x}\t{y}\n')


    plt.legend()
    plt.title('Outer Electron Spectrum')
    plt.xlabel('Electron Energy (eV)')
    plt.ylabel('Number of Electrons(1/inc.photon/eV)')
    plt.xlim(0)
    plt.savefig(os.path.join(save_folder, 'Outer_Electron_Spectrum.png'))
    plt.close()

    # OUTER ELECTRON YIELD
    previous_material = data_to_plot[0][0]
    var = []
    y = []
    for i in range(len(data_to_plot)):
        current_material = data_to_plot[i][0]
        if current_material != previous_material or i == len(data_to_plot)-1:
            # make plot of yield
            if i != len(data_to_plot) -1 :
                plt.plot(var, y, linestyle = '-', marker = 'o', label = previous_material)
                # save the data
                with open(os.path.join(save_folder, f'yield_{previous_material}_vs_{chosen_variable_settings(chosen_variable)[0]}.txt'), 'w') as file:
                    for x, y in zip(var, y):
                        file.write(f'{x}\t{y}\n')
            else:
                var.append(data_to_plot[i][1])
                y.append(data_to_plot[i][3])
                plt.plot(var, y, linestyle = '-', marker = 'o', label = previous_material)
                # save the data
                with open(os.path.join(save_folder, f'yield_{previous_material}_vs_{chosen_variable_settings(chosen_variable)[0]}.txt'), 'w') as file:
                    for x, y in zip(var, y):
                        file.write(f'{x}\t{y}\n')
                break
            #retore all to null
            var = []
            y = []
            var.append(data_to_plot[i][1])
            y.append(data_to_plot[i][3])
            previous_material = current_material
        else:
            var.append(data_to_plot[i][1])
            y.append(data_to_plot[i][3])
    plt.title('Outer Electron Yield')
    plt.legend()
    plt.ylabel('Yield (1/inc.photon)')
    plt.xlabel(chosen_variable_settings(chosen_variable)[0]+f' ({chosen_variable_settings(chosen_variable)[2]})')
    plt.savefig(os.path.join(save_folder, 'Outer_Electron_Yield.png'))
    plt.close()

    return

def read_spectrum(time_to_read, analyzed_folder):
    time = []

    for i in range(len(analyzed_folder)):
        time.append(analyzed_folder[i][0])
    
    if time_to_read == None:
        return time[-1]
    else:
        return min(time, key = lambda t: abs(t - time_to_read))

def create_analysis_folder():
    time_stamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    folder_name = f'Analysis_{time_stamp}'

    os.makedirs(folder_name, exist_ok=True)

    return folder_name
        
def create_time_analysis_folder(analysis_folder, make_evolution_plots):

    if make_evolution_plots == False:
        return

    folder_name = 'time_analysis'
    new_folder_path = os.path.join(analysis_folder, folder_name)
    os.makedirs(new_folder_path, exist_ok = True)

    return new_folder_path

def plot_time_analysis(make_evolution_plots, ALL_DATA, analyzed_data, chosen_variable, save_folder):

    if make_evolution_plots == False:
        print(f'Making time analysis: {make_evolution_plots}')
        return
    else:
        print(f'Making time analysis...')

    for i in range(len(ALL_DATA)):

        fig, axs = plt.subplots(2, 2, figsize=(10, 8))

        time = []
        num_ph = []
        num_e = []
        num_h =[]
        num_p = []
        E_ph = []
        E_e = []
        E_h_kin = []
        E_h_pot = []
        E_p = []
        E_at = []
        E_tot = []
        e_yield = []
        avg_E_escaped = []
        material = reading.read_material(ALL_DATA[i][0])

        total_all = ALL_DATA[i][1][3]
        for j in range(len(total_all)):
            time.append(total_all[j][0])
            num_ph.append(total_all[j][1])
            num_e.append(total_all[j][2])
            num_h.append(total_all[j][3])
            num_p.append(total_all[j][4])
            E_ph.append(total_all[j][5])
            E_e.append(total_all[j][6])
            E_h_kin.append(total_all[j][7])
            E_h_pot.append(total_all[j][8])
            E_p.append(total_all[j][9])
            E_at.append(total_all[j][10])
            E_tot.append(total_all[j][11])
        
        for j in range(len(analyzed_data[i][1])):
            print(f'{j} of {len(analyzed_data[i][1])}')
            y = analyzed_data[i][1][j][1]
            e_yield.append(y)
            # calculate the average energy of the escaped electrons
            # avg E = int spectr * E / int spectr = int spectr * E / yield
            W = analyzing.work_function_library(material)
            energy = analyzed_data[i][1][j][2]
            spectrum = analyzed_data[i][1][j][3]
            weighted_spectrum = np.array(spectrum) * (np.array(energy) - W)
            if y != 0:
                avg_E = simpson(weighted_spectrum , np.array(energy) - W) / y
            else:
                avg_E = 0
            if j == len(analyzed_data[i][1])-1 and y != 0: # IF WE ARE IN THE LAST TIME OF THE ANALYZED FOLDER
                weighted_spectrum = np.array(spectrum) * (np.array(energy) )
                avg_E = simpson(weighted_spectrum , np.array(energy) ) / y
            avg_E_escaped.append(avg_E)

        
        # Add overall title
        fig.suptitle(f'Time Analysis of {reading.read_material(ALL_DATA[i][0])} for {chosen_variable_settings(chosen_variable)[1]} = {reading.variable_read(chosen_variable, ALL_DATA[i][0])} {chosen_variable_settings(chosen_variable)[2]}', fontsize=16)
        
        # Top-left plot: number of particles in the simulation box
        axs[0,0].plot(time, num_ph, label = 'photons')
        axs[0,0].plot(time, num_e, label = 'electrons')
        axs[0,0].plot(time, np.array(num_h) * 1.01, label = 'holes') # shifting a little bit the holes so that you can see them in a plot
        axs[0,0].plot(time, num_p, label = 'positrons')
        axs[0,0].set_title('Evolution of Particle Number')
        axs[0,0].set_xlabel('Time (fs)')
        axs[0,0].set_ylabel('Average Number of Particles')
        axs[0,0].legend()
        axs[0,0].set_xscale('log')


        # Top-Right plot: energy of particles in the simulation box
        axs[0,1].plot(time, E_ph, label = 'photons')
        axs[0,1].plot(time, E_e, label = 'electrons')
        axs[0,1].plot(time, E_h_kin, label = 'holes kin')
        axs[0,1].plot(time, E_h_pot, label = 'holes pot')
        axs[0,1].plot(time, E_p, label = 'positrons')
        axs[0,1].plot(time, E_at, label = 'atoms')
        axs[0,1].plot(time, E_tot, label = 'Total')
        axs[0,1].set_title('Evolution of Particle Energy')
        axs[0,1].set_xlabel('Time (fs)')
        axs[0,1].set_ylabel('Average Total Energy of Particles')
        axs[0,1].legend()
        axs[0,1].set_xscale('log')

        # Bottom-Left plot: yield vs time
        axs[1,0].plot(time, e_yield)
        axs[1,0].set_title('Evolution of Yield')
        axs[1,0].set_xlabel('Time (fs)')
        axs[1,0].set_ylabel('Yield (1/inc.photon)')
        axs[1,0].set_xscale('log')

        # Bottom-Left plot: yield vs time
        axs[1,1].plot(time, avg_E_escaped)
        axs[1,1].set_title('Average Energy of Escaped Electrons')
        axs[1,1].set_xlabel('Time (fs)')
        axs[1,1].set_ylabel('Average Energy (eV)')
        axs[1,1].set_xscale('log')
        plt.tight_layout()

        path_to_save = os.path.join(save_folder, 'time_analysis')
        plt.savefig(os.path.join(path_to_save, f'evolution_{material}_{chosen_variable_settings(chosen_variable)[1]}={reading.variable_read(chosen_variable, ALL_DATA[i][0])}.png'))
    return

def make_GIFs_evolution_of_spectra(analyzed_data, chosen_variable, save_folder, make_GIFs):
    if make_GIFs == False:
        print(f'Making GIFs: {make_evolution_plots}')
        return
    else:
        print(f'Making GIFs of Spectra...')
    
    # Dictionary to track figures and axes by time_i
    plots = {}
    y_spectrum_limit = 0

    # Iterations
    for i in range(len(analyzed_data)):
        analyzed_folder = analyzed_data[i][1]

        for time, _, _, _, _ in analyzed_folder:
            if time not in plots:
            # Only ONE subplot now
                fig, ax_left = plt.subplots(figsize=(6, 5))
                plots[time] = (fig, ax_left)

            # Set title and labels
                fig.suptitle(f'Spectra at Time = {time} fs')

                ax_left.set_title('Surface Escaped Spectrum')
                ax_left.set_xlabel('Electron Energy (eV)')
                ax_left.set_ylabel('Spectrum (1/inc.photon/eV)')

            fig, ax_left = plots[time]

        # Find corresponding index for this time
            idx = next(j for j, (time_dummy, _, _, _, _) in enumerate(analyzed_folder) if time_dummy == time)

        # Read other data
            W = analyzing.work_function_library(reading.read_material(analyzed_data[i][0]))
            variable = reading.variable_read(chosen_variable, analyzed_data[i][0])
            material = reading.read_material(analyzed_data[i][0])
            my_label = chosen_variable_settings(chosen_variable)[1] + f'({material}, {round(time, 1)} fs) = {variable} ' + chosen_variable_settings(chosen_variable)[2]

            spectrum_out = np.array(analyzed_folder[idx][3])
            energy = np.array(analyzed_folder[idx][2]) - W
            # HERE FIX THE ISSUE WITH THE SPECTRUM SHIFT, IT HAS TO BE FROM ANLYZED DATA LAST NOT SHIFTED!!!
            if idx == len(analyzed_folder)-1:
                energy = analyzed_folder[idx][2]
        # Plot on the left axis
            ax_left.plot(np.array(energy), np.array(spectrum_out), label=my_label, linestyle='-')

            if max(spectrum_out) > y_spectrum_limit:
                y_spectrum_limit = max(spectrum_out)
        
    # Save all figures
    for time, (fig, ax_left) in plots.items():
        ax_left.legend()
        filename = f"time_{time:.1f}.png"
        save_path = os.path.join(save_folder, filename)
        ax_left.set_ylim(0, y_spectrum_limit*1.02)
        #ax_left.tight_layout()
        fig.savefig(save_path)
        plt.close(fig)

    # Set the save path
        save_path = save_folder
    #print('Collecting images...')

    # Collect and sort all PNG files based on time in filename
    image_files = sorted(
        glob(os.path.join(save_path, "time_*.png")),
        key=lambda x: float(re.search(r"time_([0-9.]+)\.png", os.path.basename(x)).group(1))
    )

    #print(f"Found {len(image_files)} images.")


    # Create and save GIF
    gif_path = os.path.join(save_path, "spectrum_over_time.gif")
    with imageio.get_writer(gif_path, mode='I', duration=1.0) as writer:
        for filename in image_files:
            image = imageio.imread(filename)
            writer.append_data(image)


    # Delete all the image files
    for filename in image_files:
        try:
            os.remove(filename)
            #print(f"Deleted: {filename}")
        except Exception as e:
            print(f"Error deleting {filename}: {e}")



    return