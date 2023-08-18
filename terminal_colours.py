'''
This somewhat depends on what platform you are on.
The most common way to do this is by printing ANSI escape sequences.
For a simple example, here's some Python code from the Blender build scripts:
'''
class bcolours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'