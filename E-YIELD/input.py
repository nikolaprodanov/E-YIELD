# ----------------------------------------------
#           INPUT settings for E-YIELD
# ----------------------------------------------

# The variable we want to vary for the study of the spectrum and yield
chosen_variable = 1 # 0 = material thickness(z2-z1), 1 = incoming particle irradiation energy, 2 = polar angle of incidence, # 3 = Monte Carlo iterations

# Time to read the electron spectrum [fs]
time_to_read = None # None = it is going to analyze for the last time in the simulation, [Float] = Finds the closest time_to_read to [float] from the data

# ------------------------------------------------------------
#                 Time Analysis Settings
# ------------------------------------------------------------

# Analyze spectrum and yield of 1)escaped and 2) Simulation box electrons
make_evolution_plots = True

# Make GIFs of: 1) escaped electron spectrum 2) Simulation box electron spectrum
make_GIFs = False

# ------------------------------------------------------------
#                 Version of TREKIS-4
# ------------------------------------------------------------

version = 0 # 0 = If TREKIS-4 reads through INPUT_DATA.txt and NUMERICAL_PARAMETERS.txt, 1 = If TREKIS-4 reads through INPUT.txt