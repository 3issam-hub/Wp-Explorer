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
import re
import time
import json
import emoji

#--------------------------#
#      Configuration       #
#--------------------------#

# you can change the both numbers for the numbers you want
MAX_USERS_TO_CHECK = 10
REQUEST_DELAY = 1 

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

    print(Fore.WHITE + "="*40)
    print(Fore.YELLOW + "WARNING: Use only with explicit authorization")
    print(Fore.YELLOW + "Unauthorized scanning is illegal!")
    print(Fore.WHITE + "="*40)





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
        print(Fore.CYAN + "  -v, \t--version\tDetect WordPress version\n")
        print(Fore.CYAN + "  -u, \t--users\t\tEnumerate user accounts\n")
        print(Fore.CYAN + "  -p, --plugins\tCheck for common plugins")
        #print(Fore.CYAN + "  -t, --themes\t\tCheck for common themes")
        #print(Fore.CYAN + "  -x, --xmlrpc\t\tCheck XML-RPC status")
        #print(Fore.CYAN + "  -j, --json\t\tOutput results in JSON format")
        #print(Fore.CYAN + "  --delay\t\tSet delay between requests (default 1s)\n")
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
                for site in all_results:
                    file.write(f"\nSite: {site['url']}\n")
                    file.write(f"WordPress: {'Yes' if site['is_wordpress'] else 'No'}\n")
                    if site['version']:
                        file.write(f"Version: {site['version']}\n")
                    if site['users']:
                        file.write(f"Users: {', '.join(site['users'])}\n")
                    if site['plugins']:
                        file.write(f"Plugins: {', '.join(site['plugins'])}\n")
                    file.write("Paths:\n")
                    for path in site['paths']:
                        file.write(f"  {path[0]} -> {path[1]}\n")
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

#---------------------#
#  Version detection  #
#---------------------#

def get_wordpress_version(website):
    try:
        response = requests.get(website)
        if response.status_code == 200:
            match = re.search(r'<meta name="generator" content="WordPress (\d+\.\d+\.?\d*)"', response.text)
            if match:
                return match.group(1)

        response = requests.get(f"{website}readme.html")
        if response.status_code == 200:
            match = re.search(r'Version (\d+\.\d+)', response.text)
            if match:
                return match.group(1)

        response = requests.get(f"{website}feed/")
        if response.status_code == 200:
            match = re.search(r'<generator>https://wordpress.org/\?v=(\d+\.\d+\.\d+)</generator>', response.text)
            if match:
                return match.group(1)

        return "Not detected"
    except requests.RequestException:
        return "Error checking version"

#---------------------#
#  User Enumeration   #
#---------------------#

def enumerate_users(website):
    users = set()
    try:
        for user_id in range(1, MAX_USERS_TO_CHECK + 1):
            time.sleep(REQUEST_DELAY)
            url = f"{website}?author={user_id}"
            response = requests.get(url, allow_redirects=False)
            
            if 300 <= response.status_code < 400:
                redirect = response.headers.get('Location', '')
                username = redirect.strip('/').split('/')[-1]
                if username.isnumeric():
                    continue
                users.add(username)
                print(Fore.GREEN + f"Found user: {username}")
    except Exception as e:
        print(Fore.RED + f"User enumeration error: {str(e)}")
    return list(users)

#----------------------#
#  Plugin/Theme Check  #
#----------------------#

def check_resources(website, resource_type):
    resources = []
    file_name = f"{resource_type}.txt"
    
    if not os.path.exists(file_name):
        print(Fore.RED + f"{file_name} not found!")
        return resources

    with open(file_name, 'r') as f:
        paths = [line.strip() for line in f if line.strip()]

    for path in paths:
        time.sleep(REQUEST_DELAY)
        url = f"{website}{path}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(Fore.GREEN + f"Found {resource_type[:-1]}: {url}")
                resources.append(path.split('/')[-2]) 
                plugin_name = path.split('/')[-2]

                if 'readme.txt' in path:
                    version = re.search(r'Stable tag: (\d+\.\d+\.\d+)', response.text)
                    if version:
                        versioned_entry = f"{plugin_name} ({version.group(1)})"
                        resources.append(versioned_entry)
                        print(Fore.GREEN + f"Found {resource_type[:-1]}: {versioned_entry}")
                        continue
                        
                resources.append(plugin_name)
                print(Fore.GREEN + f"Found {resource_type[:-1]}: {plugin_name}")

        except requests.RequestException:
            continue
            
    return resources

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
    try:
        for site in websites:
            site_data = {
                'url': site,
                'is_wordpress': False,
                'version': None,
                'users': [],
                'plugins': [],
                'paths': []
            }
            print(Fore.BLUE + emoji.emojize('\n🚀 ') +f"Checking if {site} is running WordPress...\n")
            if is_wordpress(site):
                site_data['is_wordpress'] = True
                print(Fore.GREEN + emoji.emojize('\n✔️  ') + f"Yes, {site} is running WordPress :) .\n")
                
                if '-v' in sys.argv or '--version' in sys.argv:
                    version = get_wordpress_version(site)
                    print(Fore.CYAN + f"WordPress version: {version}")
                    site_data['version'] = version

                if '-u' in sys.argv or '--users' in sys.argv:
                    users = enumerate_users(site)
                    print(Fore.CYAN + f"Discovered users: {', '.join(users)}")
                    site_data['users'] = users

                if '-p' in sys.argv or '--plugins' in sys.argv:
                    plugins = check_resources(site, 'plugins')
                    site_data['plugins'] = plugins
                    print(Fore.CYAN + f"Discovered plugins: {', '.join(plugins)}")

            else:
                print(Fore.RED + emoji.emojize('\n❌ ') + f"No, {site} does not appear to be running WordPress :( .\n")
                all_results.append(site_data)
                continue
            print(Fore.BLUE + f"\nChecking paths for {site}...\n")
            
            try:
                results = check_paths(site, paths, method=get_method_from_args())
                site_data['paths'] = results
                all_results.append(site_data)
            except KeyboardInterrupt:
                print(Fore.RED + "\nOperation interrupted by user.")
                sys.exit(1)

    except KeyboardInterrupt:
        print(Fore.RED + "\nProcess terminated by user. Exiting gracefully.")
        sys.exit(1)

    save_file(all_results)