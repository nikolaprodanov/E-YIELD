import os
from datetime import datetime
import reading
import analyzing
import matplotlib.pyplot as plt

def chosen_variable_settings(chosen_variable):
    variable_settings = {
        0 : ['thickness', 'd', 'A'],
        1 : ['Irradiation', 'irr', 'eV']
    }
    return variable_settings.get(chosen_variable, f'There are no settings for {chosen_variable} as chosen variable.' )

def plot_and_save_outer_spectrum_and_yield(analyzed_data, time_to_read, chosen_variable, save_folder):
    # material, variable, energy, spectrum, 
    data_to_plot = []
    for i in range(len(analyzed_data)):

        analyzed_folder = analyzed_data[i][1]
        material = reading.read_material(analyzed_data[i][0])
        variable = reading.read_thickness_z(analyzed_data[i][0]) # modify this 
        
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
        
def create_time_analysis_folder(analysis_folder):

    folder_name = 'time_analysis'
    new_folder_path = os.path.join(analysis_folder, folder_name)
    os.makedirs(new_folder_path, exist_ok = True)

    return new_folder_path
