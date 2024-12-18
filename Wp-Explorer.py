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
                if method == "POST":
                    response = requests.get(full_url, timeout=5)
                else:
                    response = requests.get(full_url, timeout=5)
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
        print(Fore.RED + "\nExiting...........................!")
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
        except KeyboardInterrupt:
            print(Fore.RED + "\nExiting.................................!")
            sys.exit(0)

    return False

#-----------------#
#      Main       #
#-----------------#

if __name__ == "__main__":
    art()
    help()

    if len(sys.argv) < 2:
        print(Fore.RED + "Error: Please provide the website URL as an argument.")
        print(Fore.YELLOW + "Usage: python3 Wp-Explorer.py http://example.com\n")
        sys.exit(1)

    website = sys.argv[1].strip()

    if not os.path.exists('paths.txt'):
        print(Fore.RED + "Error: 'paths.txt' file is missing. Please add it to the same directory.\n")
        sys.exit(1)

    print(Fore.BLUE + "\nChecking if the website is running WordPress...\n")
    if is_wordpress(website):
        print(Fore.GREEN + "Yes, the website is running WordPress :) .\n")
    else:
        print(Fore.RED + "No, the website does not appear to be running WordPress :( .\n")

    def read_paths(file_path):
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]

    paths = read_paths('paths.txt')
    print(Fore.BLUE + "\nChecking paths...\n")
    
    try:
        results = check_paths(website, paths)
    except KeyboardInterrupt:
        results = check_paths(website, paths)

    save_file(results)