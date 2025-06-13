import os

def get_valid_folders(base_dir="OUTPUT_TREKIS"):
    return [
        name for name in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, name))
    ]

def read_material(folder_name, base_dir="OUTPUT_TREKIS"):
    """
    Reads the first line (index 1) of INPUT_DATA.txt in a specified subfolder and returns the part before '!'.

    Args:
        folder_name (str): The name of the subfolder inside OUTPUT_TREKIS.
        base_dir (str): Base directory. Defaults to 'OUTPUT_TREKIS'.

    Returns:
        str: The part of the line before the '!' character, stripped of whitespace.
    """
    file_path = os.path.join(base_dir, folder_name, "INPUT_DATA.txt")
    
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            if len(lines) > 1:
                line = lines[1]  # First line after the header
                before_exclamation = line.split('!')[0].strip()
                return before_exclamation
            else:
                print("The file doesn't have enough lines.")
                exit()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        exit()
    except Exception as e:
        print(f"An error occurred: {e}")
        exit()

def read_thickness_z(folder_name, base_dir="OUTPUT_TREKIS"):
    """
    Reads the 9th line (index 8) of INPUT_DATA.txt and returns the difference float(b) - float(a),
    where the line format is: <a> <b> !comments

    Args:
        folder_name (str): Name of the subfolder inside OUTPUT_TREKIS.
        base_dir (str): Base directory. Defaults to 'OUTPUT_TREKIS'.

    Returns:
        float: The difference b - a.
    """
    file_path = os.path.join(base_dir, folder_name, "INPUT_DATA.txt")

    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            if len(lines) > 9:
                line = lines[9].split("!")[0].strip()  # Get content before comment
                parts = line.split()
                if len(parts) >= 2:
                    a = float(parts[0])
                    b = float(parts[1])
                    return b - a
                else:
                    print("Line doesn't contain two numeric values.")
                    exit()
            else:
                print("The file doesn't have enough lines.")
                exit()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        exit()
    except ValueError:
        print("Could not convert values to float.")
        exit()
    except Exception as e:
        print(f"An error occurred: {e}")
        exit()

def read_energy(folder_name, base_dir="OUTPUT_TREKIS"):
    """
    Reads the first line (index 1) of INPUT_DATA.txt in a specified subfolder and returns the part before '!'.

    Args:
        folder_name (str): The name of the subfolder inside OUTPUT_TREKIS.
        base_dir (str): Base directory. Defaults to 'OUTPUT_TREKIS'.

    Returns:
        str: The part of the line before the '!' character, stripped of whitespace.
    """
    file_path = os.path.join(base_dir, folder_name, "INPUT_DATA.txt")
    
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            if len(lines) > 1:
                line = lines[21]  # First line after the header
                before_exclamation = line.split('!')[0].strip()
                return before_exclamation
            else:
                print("The file doesn't have enough lines.")
                exit()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        exit()
    except Exception as e:
        print(f"An error occurred: {e}")
        exit()

def read_polar_angle(folder_name, base_dir="OUTPUT_TREKIS"):
    """
    Reads the first line (index 1) of INPUT_DATA.txt in a specified subfolder and returns the part before '!'.

    Args:
        folder_name (str): The name of the subfolder inside OUTPUT_TREKIS.
        base_dir (str): Base directory. Defaults to 'OUTPUT_TREKIS'.

    Returns:
        str: The part of the line before the '!' character, stripped of whitespace.
    """
    file_path = os.path.join(base_dir, folder_name, "INPUT_DATA.txt")
    
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            if len(lines) > 1:
                line = lines[20]  # First line after the header
                before_exclamation = line.split('!')[0].strip()
                return before_exclamation
            else:
                print("The file doesn't have enough lines.")
                exit()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        exit()
    except Exception as e:
        print(f"An error occurred: {e}")
        exit()

def read_simulation_time(folder_name, base_dir="OUTPUT_TREKIS"):

    """
    Reads the first number in the first column from the last line of 'OUTPUT_total_all.dat'
    in the given folder.

    Args:
        folder_name (str): Name of the subfolder inside OUTPUT_TREKIS.
        base_dir (str): Base directory. Defaults to 'OUTPUT_TREKIS'.

    Returns:
        float: First number in the first column of the last line.
    """
    file_path = os.path.join(base_dir, folder_name, "OUTPUT_total_all.dat")
    
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            if not lines:
                print("The file is empty.")
                exit()
            last_line = lines[-1].strip()
            parts = last_line.split()
            if parts:
                return float(parts[0])
            else:
                print("The last line is empty or malformed.")
                exit()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        exit()
    except ValueError:
        print("Could not convert value to float.")
        exit()
    except Exception as e:
        print(f"An error occurred: {e}")
        exit()

def print_folders_and_significant_data(folder_names, base_dir="OUTPUT_TREKIS"):
    """
    Prints folder names and selected values from each folder using custom-defined functions.
    
    Args:
        folder_names (list of str): List of subfolder names inside OUTPUT_TREKIS.
    """
    i = 0
    for folder in folder_names:
        #material = read_material(folder)
        simulation_time = read_simulation_time(folder)
        d = read_thickness_z(folder)
        theta = read_polar_angle(folder)
        #energy = read_energy(folder)
        i = i + 1
        print(f"{i}) Folder:{folder} | Sim-Time:{simulation_time} fs | d = {d} A | theta = {theta}")

def extract_data_from(folder_name, base_dir="OUTPUT_TREKIS"):

    """
    Extracts data from 4 specific files in a folder, skipping comment lines starting with '#' and empty lines.
    
    Returns:
        list: A list of 2D lists (one per file), so you can access columns easily.
    """

    material = read_material(folder_name)

    file_names = [
        "OUTPUT_electron_spectrum_1d_Z.dat",    # all_data[0]
        f"OUTPUT_electron_spectrum_{material}.dat",      # all_data[1]
        f"OUTPUT_DOS_of_{material}.dat",                  # all_data[2]
        "OUTPUT_total_all.dat"                   # all_data[3]
    ]

    file_data_list = []

    for file_name in file_names:
        file_path = os.path.join(base_dir, folder_name, file_name)
        data = []

        try:
            with open(file_path, "r") as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comment lines starting with '#'
                    if line and not line.startswith("#"):
                        try:
                            values = list(map(float, line.split()))
                            data.append(values)
                        except ValueError:
                            print(f"Warning: Skipping malformed line in {file_path}: {line}")
        except FileNotFoundError:
            print(f"Warning: File not found: {file_path}")
            data = None

        file_data_list.append(data)

    return file_data_list

def extract_data_all_folders(folder_names, base_dir="OUTPUT_TREKIS"):

    """
    Extract data from all valid subfolders inside base_dir.

    Returns:
        list of tuples: [(folder_name, data), ...]
        where data is the list returned by extract_all_data(folder_name)
    """
    all_folders_data = []

    for folder_name in folder_names:
        data = extract_data_from(folder_name, base_dir="OUTPUT_TREKIS")
        all_folders_data.append((folder_name, data))

    return all_folders_data

def variable_read(chosen_variable, folder_name):
    if chosen_variable == 0:
        return read_thickness_z(folder_name)
    if chosen_variable == 1:
        return read_energy(folder_name)
    if chosen_variable == 2:
        return read_polar_angle(folder_name)
    if chosen_variable == 3:
        return read_Monte_Carlo(folder_name)