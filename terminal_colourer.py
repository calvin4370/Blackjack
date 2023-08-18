from terminal_colours import bcolours

class Colour:
    def purple(message):
        # also known as HEADER
        return f'{bcolours.HEADER}{message}{bcolours.ENDC}'

    def blue(message):
        return f'{bcolours.OKBLUE}{message}{bcolours.ENDC}'

    def cyan(message):
        return f'{bcolours.OKCYAN}{message}{bcolours.ENDC}'

    def green(message):
        return f'{bcolours.OKGREEN}{message}{bcolours.ENDC}'
    
    def yellow(message):
        # also known as WARNING
        return f'{bcolours.WARNING}{message}{bcolours.ENDC}'

    def red(message):
        # also known as FAIL
        return f'{bcolours.FAIL}{message}{bcolours.ENDC}'
    
    def bold(message):
        return f'{bcolours.BOLD}{message}{bcolours.ENDC}'

    def underline(message):
        return f'{bcolours.UNDERLINE}{message}{bcolours.ENDC}'