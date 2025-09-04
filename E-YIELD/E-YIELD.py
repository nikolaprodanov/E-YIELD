# ------------------------------------------------------------
#         E-YIELD: Data Analysis Software for TREKIS-4
# ------------------------------------------------------------

# This Software is available on: 
# Version: August 2025
# Read README.dat for instructions
# Contact for bugs, fixes or requests: nikola.prodanov2023@gmail.com
# TREKIS-4 Software available on: 
# Good Luck with Simulations! :)

# ------------------------------------------------------------
#                Inputs and Libraries
# ------------------------------------------------------------
from input import chosen_variable, time_to_read, make_evolution_plots, make_GIFs
import reading
import analyzing
import plotting 
# ------------------------------------------------------------
#                       MAIN PROGRAM
# ------------------------------------------------------------

#print.welcome()

# ------------------------------------------------------------
#                     Reading the Files
# ------------------------------------------------------------

# Get folder names in OUTPUT_TREKIS, # key for the data
folder_names = reading.get_valid_folders()

# Print the folder names with significant data inside for check
reading.print_folders_and_significant_data(folder_names)

# Extract all data from all folders
ALL_DATA = reading.extract_data_all_folders(folder_names)
# you get [folder_name, data_folder]
# data_folder = [spectrum in Z, spectrum_material, DOS, Total All] # add the energy density

# ------------------------------------------------------------
#                       Analyzing data
# ------------------------------------------------------------

# Calculate Yield and prepare data for plotting
analyzed_data = analyzing.data_all_folders(ALL_DATA)
# analyzed_data = [folder_name, analyzed_folder]
# analyzed_folder = [time, yield, energy, spectrum_out, spectrum_material] 

# ------------------------------------------------------------
#                 Plotting and Saving Data
# ------------------------------------------------------------

# Creating a Folder where to save all the results
save_folder = plotting.create_analysis_folder()

# Making Plots and saving data
plotting.plot_and_save_outer_spectrum_and_yield(analyzed_data, time_to_read, chosen_variable, save_folder)

# Time Analysis Folder
time_folder = plotting.create_time_analysis_folder(save_folder, make_evolution_plots)

# Time Analysis Plotting
plotting.plot_time_analysis(make_evolution_plots, ALL_DATA, analyzed_data, chosen_variable, save_folder)

# ------------------------------------------------------------
#                   Playground of E-YIELD
# ------------------------------------------------------------

# Production of GIF for the outer electron spectra
plotting.make_GIFs_evolution_of_spectra(analyzed_data, chosen_variable, save_folder, make_GIFs)

# ------------------------------------------------------------
#                       Exiting E-YIELD
# ------------------------------------------------------------

# print.goodbye()
