BOLD = '\033[1m'
WARNING = '\033[93m'
ERROR = '\033[91m'
OK = '\033[32m'
END = '\033[0m'
INFO = '\033[37m'

def print_info(text :str):
    print(INFO + text + END)

def print_error(text :str):
    print(ERROR + text + END)

def print_ok(text :str):
    print(OK + text + END)

def print_warning(text :str):
    print(WARNING + text + END)

def print_bold(text :str):
    print(BOLD + text + END)

def user_continue() -> bool:
    ans = input("\nContinue? [y/N]\n")
    if (ans in ['yes', 'y', 'Y', 'YES']):
        return True
    return False

def print_header(element :str): 
    print_info('\n------------------------------------\n'
                + element + 
               '\n------------------------------------') 