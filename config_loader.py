# Function: load_config
# Description: loads configuration settings from a specified file.
#              It reads the file line by line, ignoring comments and empty lines.
#              Each valid line is expected to have a key-value pair separated by an '='.
#              The function returns a dictionary with the configuration settings.
# Parameters: 
#    - file_path (str): the path to the configuration file
# Returns:
#    - config (dict): a dictionary containing configuration key-value pairs
def load_config(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip() # remove leading/trailing whitespace from the line
            # check if the line is not empty and doesn't start with a comment character '#'
            if line and not line.startswith("#"):
                # split the line into key and value using '=' as the delimiter
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    return config
