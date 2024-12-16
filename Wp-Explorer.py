#!/home/codespace/.python/current/bin/python

#--------------------------#
#  libraries importation   #
#--------------------------#

from colorama import Fore, Style, init
import requests
import pyfiglet
import random
import sys
import os



#--------#
#  ART   #
#--------#

def art():
    # Initialize colorama
    init(autoreset=True)
    # Generate ASCII art
    ascii_art = pyfiglet.figlet_format("Wp-Explorer", font='standard')
    # Define a list of colors
    colors = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    # Print each line of ASCII art in a random color
    for line in ascii_art.splitlines():
        if line.strip():  # Check if the line is not empty
            print(random.choice(colors) + line)
    # Reset color
    print(Style.BRIGHT+Style.RESET_ALL)
    print(Fore.RED+'                                                 By Issam_Beniysa\n\n\n')

#------------------#
#  Help And Menu   #
#------------------#

def help():
    if '-h' in sys.argv or '--help' in sys.argv:
        print(Fore.CYAN + "{Usage} : python3 Wp_Explorer.py [Website] [Options] \n\n")
        print(Fore.CYAN + "{Options} : \n")
        print(Fore.CYAN + "  -h, \t--help\t\tShow this help message and exit\n")
        print(Fore.CYAN + "  -o, \t--output\tTo save result in a specific file\n")
        sys.exit(0)

#----------------#
#  check paths   #
#----------------#

def check_paths(website, paths):
    # Ensure the website has a trailing slash if missing
    if not website.endswith('/'):
        website += '/'

    results = []

    for path in paths:
        full_url = website + path
        try:
            response = requests.get(full_url, timeout=5)
            status_code = response.status_code

            if status_code == 200:
                print(Fore.GREEN + f"{full_url} -> {status_code}")
            elif status_code == 404:
                print(Fore.RED + f"{full_url} -> {status_code}")
            else:
                print(Fore.YELLOW + f"{full_url} -> {status_code}")
            sys.stdout.flush()

        except requests.RequestException as e:
            print(Fore.RED + f"{full_url} -> Error: {str(e)}")
            sys.stdout.flush()
        except KeyboardInterrupt:
            print(Fore.RED + "Exiting.................................!")
            sys.exit(0)

    return results

#------------------------#
#  xheck Wp is running   #
#------------------------#

def is_wordpress(website):
    # Ensure the website has a trailing slash if missing
    if not website.endswith('/'):
        website += '/'

    wordpress_indicators = [
        "wp-login.php",    # WordPress login page
        "wp-admin/",       # WordPress admin dashboard
        "wp-content/",     # WordPress content folder
    ]

    for indicator in wordpress_indicators:
        url = website + indicator
        try:
            response = requests.get(url, timeout=5)
            # Check for HTTP 200/403/401 to verify the file/folder exists
            if response.status_code in [200, 403, 401]:
                return True
        except requests.RequestException:
            # Ignore errors like timeouts or DNS issues
            continue
        except KeyboardInterrupt:
            print(Fore.RED + "Exiting.................................!")
            sys.exit(0)

    # If no indicators were found
    return False

if __name__ == "__main__":
    
    help()

    if len(sys.argv) < 2:
        print(Fore.RED + "Error: Please provide the website URL as an argument.")
        print(Fore.YELLOW + "Usage: python3 Wp-Explorer http://example.com\n")
        sys.exit(1)  
    website = sys.argv[1].strip()
    if not os.path.exists('paths.txt'):
        print(Fore.RED + "Error: 'paths.txt' file is missing. Please add it to the same directory.\n")
        sys.exit(1)

    art()
    
    print(Fore.BLUE + "\nChecking if the website is running Wordpress.................................\n")
    result = is_wordpress(website)
    if result:
        print(Fore.GREEN +"Yes, the website is running WordPress :) .\n")
    else:
        print(Fore.RED +"No, the website does not appear to be running WordPress :( .\n")
    
    def read_paths(file_path):
        with open(file_path, 'r') as file:  # Open the file in read mode
        # Read lines and strip whitespace
            return [line.strip() for line in file if line.strip()]  # Return non-empty lines

    paths = read_paths('paths.txt')
    print(Fore.BLUE + "\nChecking paths...\n")
    check_paths(website, paths)
