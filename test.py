#!/bin/python3

#--------------------------#
#  libraries importation   #
#--------------------------#

from colorama import Fore, Style, init
import requests
import pyfiglet
import random
import sys

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
            results.append((full_url, response.status_code))
        except requests.RequestException as e:
            # Handle errors such as timeouts or connection issues
            results.append((full_url, str(e)))
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
    art()
    
    website = input("Enter the base website (e.g., https://example.com): ").strip()
    print(Fore.BLUE + "\nChecking if the website is running Wordpress.................................\n")
    result = is_wordpress(website)
    if result:
        print(Fore.GREEN +"Yes, the website is running WordPress :) .\n")
    else:
        print(Fore.RER +"No, the website does not appear to be running WordPress :( .\n")
    
    def read_paths(file_path):
        with open(file_path, 'r') as file:  # Open the file in read mode
        # Read lines and strip whitespace
            return [line.strip() for line in file if line.strip()]  # Return non-empty lines

    paths = read_paths('paths.txt')

    results = check_paths(website, paths)

    for url, status in results:
        print(f"{url} -> {status}\n")