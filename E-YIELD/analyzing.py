from scipy.integrate import simpson
import reading

def work_function_library(material):
    work_functions ={
        'Si': 4.76, #eV
        'SiO2': 5.0
    }

    return work_functions.get(material, f'Work function for {material} not found, please insert it in analyzing.py/work_function_library function.')

def yield_and_spectrum_sorting(spectrum_z, spectrum_material, folder_name):
    # spectrum: time_i energy_j spectrum_j
    energy = []
    spec = []
    spec_material = []
    previous_time = spectrum_z[0][0]

    # result
    result = []
    # time, yield, spectrum_out

    size = len(spectrum_z)
    material = reading.read_material(folder_name)

    for i in range(size):
        current_time = spectrum_z[i][0]
        if current_time != previous_time or i == size - 1: # check this index
            # do the calculation of the yield
            e_yield = simpson(spec, energy) # substitute with integral simpson

            # for storing
            # time, yield, energy, spectrum_out, spectrum_material
            result.append((previous_time, e_yield, energy, spec, spec_material))
            
            # after ending append the values for the new time
            energy = []
            spec = []
            spec_material = []
            energy.append(spectrum_z[i][1])
            spec.append(spectrum_z[i][2])
            spec_material.append(spectrum_material[i][2])
            previous_time = current_time
        else:
            energy.append(spectrum_z[i][1])
            spec.append(spectrum_z[i][2])
            spec_material.append(spectrum_material[i][2])
    
    return result 

def data_all_folders(ALL_DATA):

    analyzed_data = []
    i = 0
    for i in range(len(ALL_DATA)):
        spectrum_z = ALL_DATA[i][1][0]
        spectrum_material = ALL_DATA[i][1][1]
        folder_name = ALL_DATA[i][0]
        analyzed_data.append(( ALL_DATA[i][0], yield_and_spectrum_sorting(spectrum_z, spectrum_material, folder_name) ))
    
    return analyzed_data
