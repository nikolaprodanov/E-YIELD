import os 
import numpy as np 
import matplotlib.pyplot as plt 

keywords = ['electron', 'photon', 'positron', 'hole']

current_directory = os.path.dirname(os.path.abspath(__file__))

def process_file(filename):
    data = []
    column_labels = []
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('#'):
                if not column_labels:
                    column_labels = line[1:].split()
            else: # Skips commented lines
                values = line.split()
                data.append([float(v) for v in values])
    return np.array(data), column_labels

def get_material():
    folder_name = os.path.basename(os.getcwd())

    parts = folder_name.split('_')
    if len(parts) > 1:
        return parts[-1]
    else:
        print('The directory is different.')
        exit()

def remove_a_string(string2remove,input_string):
    return input_string.replace(f'{string2remove}','')

def remove_before_and_including(suffix, filename):
    position = filename.find(suffix)
    if position != -1:
        return filename[position + len(suffix):]
    else:
        return filename

# Dictionary to hold lists of files for each keyword
keyword_files = {keyword: [] for keyword in keywords}

# Read the name of the material inside the folder
material = get_material()

for file in os.listdir(current_directory):
    if file.startswith('OUTPUT_Stopping'): # skips the stoppig power file since it contains the keyword
        continue 
    if 'NO' in file: # if a model is turned off, there is a NO in the filename, so we skip it
        continue
    if file.endswith('.dat'): # All files are in this format
        for keyword in keywords:
            if keyword in file.lower():
                keyword_files[keyword].append(os.path.join(current_directory, file))

for keyword, files in keyword_files.items():
    if files:
        plt.figure()
        plt.title(f'MFP of {keyword}s in {material}')
        plt.xlabel('Energy(eV)')
        plt.ylabel('MFP(A)')

        # Set the log scale
        plt.xscale('log')
        plt.yscale('log')

        # Set the limits of x and y
        plt.xlim(0.1,1e11)
        plt.ylim(0.1,1e11)

        for file in files:
            #print(f'Currently processing: {file}')
            data, column_labels = process_file(file)
            x = data[:, 0]
            
            for i in range(1, data.shape[1]):
                y = data[:, i]
                label = column_labels[i] if i < len(column_labels) else f'column {i+1}'
                label = remove_a_string('(A)', label)
                label = remove_a_string('_MFP', label)
                label.replace('_','')

                preffix_label = remove_before_and_including('OUTPUT_',file)
                preffix_label = remove_before_and_including('OUTPUT_',preffix_label)
                #preffix_label = remove_a_string(f'{material}_', preffix_label)
                preffix_label = remove_a_string(f'_{keyword}',preffix_label)
                preffix_label = remove_a_string('.dat', preffix_label)
                preffix_label.replace('_',' ')
                print(f'For {keyword}s in {material}: plotting the {preffix_label}: {label}.')
                plt.plot(x, y, linestyle = '-', marker = None,  label = f'{preffix_label}: {label}')
        
        plt.legend(loc='upper right')
        plt.savefig(f'MFPs_{keyword}.png')
        #plt.show()