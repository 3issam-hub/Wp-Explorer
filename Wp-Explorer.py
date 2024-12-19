#!/bin/python

#!/bin/python

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
    init(autoreset=True)
    ascii_art = pyfiglet.figlet_format("Wp-Explorer", font='standard')
    colors = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    for line in ascii_art.splitlines():
        if line.strip():
            print(random.choice(colors) + line)
    print(Style.BRIGHT + Style.RESET_ALL)
    print(Fore.RED + '                                                 By Issam_Beniysa\n\n\n')

#------------------#
#  Help And Menu   #
#------------------#

def help():
    if '-h' in sys.argv or '--help' in sys.argv:
        print(Fore.CYAN + "{Usage} : python3 Wp_Explorer.py [Website] [Options] \n\n")
        print(Fore.CYAN + "{Options} : \n")
        print(Fore.CYAN + "  -h, \t--help\t\tShow this help message and exit\n")
        print(Fore.CYAN + "  -o, \t--output\tTo save result in a specific file\n")
        print(Fore.CYAN + "  -m, \t--method\tTo Specify the HTTP method to use (GET or POST). Default is GET\n")
        print(Fore.CYAN + "  -l, \t--site-list\tProvide a list of websites from a file\n")
        sys.exit(0)

#-----------------#
#  Save in File   #
#-----------------#

def save_file(results):
    if '-o' in sys.argv or '--output-file' in sys.argv:
        try:
            index = sys.argv.index('-o') if '-o' in sys.argv else sys.argv.index('--output-file')
            output_file = sys.argv[index + 1]

            with open(output_file, 'w') as file:
                for url, status in results:
                    file.write(f"{url} -> {status}\n")
            print(Fore.GREEN + f"Results saved to {output_file}")
        except IndexError:
            print(Fore.RED + "Error: Missing filename for output. Use -o <filename>")
            sys.exit(1)
        except IOError as e:
            print(Fore.RED + f"Error: Unable to save results. {str(e)}")
            sys.exit(1)

#------------------#
#  Parse Method    #
#------------------#

def get_method_from_args():
    if '-m' in sys.argv or '--method' in sys.argv:
        try:
            index = sys.argv.index('-m') if '-m' in sys.argv else sys.argv.index('--method')
            method = sys.argv[index + 1].upper() 
            if method not in ["GET", "POST"]:
                raise ValueError("Invalid method. Only GET and POST are supported.")
            return method
        except (IndexError, ValueError) as e:
            print(Fore.RED + f"Error: {str(e)}")
            sys.exit(1)
    return "GET"

#--------------------#
#  Handle Site List  #
#--------------------#

def handle_site_list(file_path):
    try:
        with open(file_path, 'r') as file:
            websites = [line.strip() for line in file if line.strip()]
        return websites
    except FileNotFoundError:
        print(Fore.RED + f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except IOError as e:
        print(Fore.RED + f"Error: Unable to read file '{file_path}'. {str(e)}")
        sys.exit(1)

#----------------#
#  Check Paths   #
#----------------#

def check_paths(website, paths, method="GET"):
    if not website.endswith('/'):
        website += '/'

    results = []

    try:
        for path in paths:
            full_url = website + path
            try:
                response = requests.post(full_url, timeout=5) if method == "POST" else requests.get(full_url, timeout=5)
                status_code = response.status_code

                if status_code == 200:
                    print(Fore.GREEN + f"{full_url} -> {status_code}")
                elif status_code == 404:
                    print(Fore.RED + f"{full_url} -> {status_code}")
                else:
                    print(Fore.YELLOW + f"{full_url} -> {status_code}")
                results.append((full_url, status_code))
                sys.stdout.flush()

            except requests.RequestException as e:
                print(Fore.RED + f"{full_url} -> Error: {str(e)}")
                results.append((full_url, f"Error: {str(e)}"))
                sys.stdout.flush()

    except KeyboardInterrupt:
        print(Fore.RED + "\nExiting...")
        return results

    return results

#--------------------------#
#  Check if WP is Running  #
#--------------------------#

def is_wordpress(website):
    if not website.endswith('/'):
        website += '/'

    wordpress_indicators = [
        "wp-login.php",
        "wp-admin/",
        "wp-content/",
    ]

    for indicator in wordpress_indicators:
        url = website + indicator
        try:
            response = requests.get(url, timeout=5)
            if response.status_code in [200, 403, 401]:
                return True
        except requests.RequestException:
            continue

    return False

#-----------------#
#      Main       #
#-----------------#

if __name__ == "__main__":
    art()
    help()

    if len(sys.argv) < 2:
        print(Fore.RED + "Error: Please provide the website URL or site list file as an argument.")
        print(Fore.YELLOW + "Usage: python3 Wp-Explorer.py http://example.com\n")
        sys.exit(1)

    website = None
    site_list = None

    if '-l' in sys.argv or '--site-list' in sys.argv:
        try:
            index = sys.argv.index('-l') if '-l' in sys.argv else sys.argv.index('--site-list')
            site_list_file = sys.argv[index + 1]
            site_list = handle_site_list(site_list_file)
        except IndexError:
            print(Fore.RED + "Error: Missing filename for site list. Use -l <filename>")
            sys.exit(1)
    else:
        website = sys.argv[1].strip()

    if not os.path.exists('paths.txt'):
        print(Fore.RED + "Error: 'paths.txt' file is missing. Please add it to the same directory.\n")
        sys.exit(1)

    paths = handle_site_list('paths.txt')
    websites = site_list if site_list else [website]

    all_results = []
    for site in websites:
        print(Fore.BLUE + f"\nChecking if {site} is running WordPress...\n")
        if is_wordpress(site):
            print(Fore.GREEN + f"Yes, {site} is running WordPress :) .\n")
        else:
            print(Fore.RED + f"No, {site} does not appear to be running WordPress :( .\n")

        print(Fore.BLUE + f"\nChecking paths for {site}...\n")
        try:
            results = check_paths(site, paths, method=get_method_from_args())
            all_results.extend(results)
        except KeyboardInterrupt:
            print(Fore.RED + "\nOperation interrupted by user.")
            sys.exit(1)

    save_file(all_results)