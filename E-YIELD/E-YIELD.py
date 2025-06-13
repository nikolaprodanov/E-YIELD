# ------------------------------------------------------------
#         E-YIELD: Data Analysis Software for TREKIS-4
# ------------------------------------------------------------

# This Software is available on: 
# Version: June 2025
# Read README.dat for instructions
# Contact for bugs, fixes or requests: nikola.prodanov2023@gmail.com
# TREKIS-4 Software available on: 
# Good Luck with Simulations! :)

# ------------------------------------------------------------
#                        Inputs
# ------------------------------------------------------------

# The variable we want to vary for the study of the spectrum and yield
chosen_variable = 0
# 0 = material thickness(z2-z1)
# 1 = incoming particle irradiation energy 
# 2 = polar angle of incidence
# 3 = Monte Carlo iterations
# 4 = W_modified - W_original --> Produce this your own way since TREKIS-4 does not make it by default

# Time to read the electron spectrum [fs]
time_to_read = None
# Default: None, it is going to analyze for the last time in the simulation
# Otherwise it is going to find the closest to time_to_read from the data

# ------------------------------------------------------------
#                    Secondary Inputs
# ------------------------------------------------------------

# Analyze spectrum and yield of 1)escaped and 2) Simulation box electrons
make_evolution_plots = True

# Make GIFs of: 1) escaped electron spectrum 2) Simulation box electron spectrum
make_GIFs = True

# ------------------------------------------------------------
#                        Libraries
# ------------------------------------------------------------
import reading
import analyzing
import plotting 
import settings
# ------------------------------------------------------------
#                     MAIN PROGRAM
# ------------------------------------------------------------

# print.welcome()

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
# data_folder =[spectrum in Z, spectrum_material, DOS, Total All] # add the energy density

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