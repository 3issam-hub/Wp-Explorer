#!/bin/python

#--------------------------#
#  libraries importation   #
#--------------------------#

from colorama import Fore, Style, init
import configparser
import requests
import pyfiglet
import random
import sys
import os
import re
import time
import json
import csv
import emoji

#------------------------#
#      load config       #
#------------------------#
VULN_DB_URL = "https://wpvulndb.com/api/v3/plugins"

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    defaults = {
        'Api': {
            'api_key': None
        },
        'Settings': {
            'max_users_to_check': '10',
            'request_delay': '1',
            'output_format': 'text'
        }
    }

    for section, options in defaults.items():
        if section not in config:
            config[section] = {}
        for key, value in options.items():
            if key not in config[section]:
                config[section][key] = value
    
    return config

config = load_config()
MAX_USERS_TO_CHECK = int(config['Settings']['max_users_to_check'])
REQUEST_DELAY = float(config['Settings']['request_delay'])
OUTPUT_FORMAT = config['Settings']['output_format']



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
    print(Fore.WHITE + "="*40+"\n")



#----------#
#  Delay   #
#----------#

if '--delay' in sys.argv:
    try:
        index = sys.argv.index('--delay')
        REQUEST_DELAY = float(sys.argv[index + 1])
        print(Fore.CYAN + f"Request delay set to {REQUEST_DELAY} seconds")
    except (IndexError, ValueError):
        print(Fore.RED + "Error: --delay requires a numeric value (e.g., --delay 2.5)")
        sys.exit(1)

#------------------#
#  Help And Menu   #
#------------------#

def help():
    if '-h' in sys.argv or '--help' in sys.argv:
        print(Fore.CYAN + "{Usage} : python3 Wp_Explorer.py [Website] [Options] \n\n")
        print(Fore.CYAN + "{Options} : \n")
        print(Fore.CYAN + "  -h, \t--help\t\t\tShow this help message and exit\n")
        print(Fore.CYAN + "  -o, \t--output\t\tTo save result in a specific file\n")
        print(Fore.CYAN + "  -m, \t--method\t\tTo Specify the HTTP method to use (GET or POST). Default is GET\n")
        print(Fore.CYAN + "  -l, \t--site-list\t\tProvide a list of websites from a file\n")
        print(Fore.CYAN + "  -v, \t--version\t\tDetect WordPress version\n")
        print(Fore.CYAN + "  -u, \t--users\t\t\tEnumerate user accounts\n")
        print(Fore.CYAN + "  -p, \t--plugins\t\tCheck for common plugins\n")
        print(Fore.CYAN + "  -t, \t--themes\t\tCheck for common themes\n")
        print(Fore.CYAN + "  -x, \t--xmlrpc\t\tCheck XML-RPC status\n")
        print(Fore.CYAN + "  \t--delay\t\t\tSet delay between requests (default 1s)\n")
        print(Fore.CYAN + "\nConfiguration:\n")
        print(Fore.CYAN + "  Create a 'config.ini' file to customize settings:\n")
        print(Fore.CYAN + "  \t[Api]")
        print(Fore.CYAN + "  \t\tapi_key = your_wpscan_api_key\n")
        print(Fore.CYAN + "  \t[Settings]")
        print(Fore.CYAN + "  \t\tmax_users_to_check = 10")
        print(Fore.CYAN + "  \t\trequest_delay = 1")
        print(Fore.CYAN + "  \t\toutput_format = text")
        sys.exit(0)


#------------------#
#  vuln db check   #
#------------------#

def check_vuln_db(plugin_name, version):
    api_key = config['Api'].get('api_key')
    
    if not api_key:
        print(Fore.YELLOW + "WPScan API key not found in config.ini. Skipping vulnerability checks.")
        return None
    
    try:
        
        headers = {
            "Authorization": f"Token token={api_key}",
            "Content-Type": "application/json"
        }
        plugin_slug = plugin_name.lower().replace(" ", "-")
        url = f"{VULN_DB_URL}/{plugin_slug}"  
        
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  
        
        data = response.json()
        vulnerabilities = []
        
        if plugin_slug in data:
            plugin_data = data[plugin_slug]
            for vuln in plugin_data.get("vulnerabilities", []):
                
                if version in vuln.get("fixed_in", []):
                    continue  
                if version in vuln.get("affected_versions", []):
                    vulnerabilities.append({
                        "id": vuln.get("id"),
                        "title": vuln.get("title"),
                        "description": vuln.get("description"),
                        "severity": vuln.get("severity"),
                        "fixed_in": vuln.get("fixed_in"),
                        "references": vuln.get("references")
                    })
        
        return vulnerabilities if vulnerabilities else None
    
    except requests.RequestException as e:
        print(Fore.RED + f"Error checking vulnerabilities for {plugin_name}: {str(e)}")
        return None

#-----------------#
#  Save in File   #
#-----------------#
def save_file(results):
    if '-o' in sys.argv or '--output' in sys.argv:
        try:
            index = sys.argv.index('-o') if '-o' in sys.argv else sys.argv.index('--output')
            output_file = sys.argv[index + 1]

            if output_file.endswith('.json'):
                
                with open(output_file, 'w') as file:
                    json.dump(results, file, indent=4)
                print(Fore.GREEN + f"Results saved to {output_file} (JSON format)")

            elif output_file.endswith('.csv'):
                
                with open(output_file, 'w', newline='') as file:
                    writer = csv.writer(file)
                    
                    writer.writerow([
                        "Site", "WordPress", "Version", "Users", "Plugins", "Themes", 
                        "Vulnerabilities", "XML-RPC Status", "Paths"
                    ])
                    
                    for site in results:
                        writer.writerow([
                            site['url'],
                            'Yes' if site['is_wordpress'] else 'No',
                            site.get('version', 'N/A'),
                            ', '.join(site.get('users', [])),
                            ', '.join(site.get('plugins', [])),
                            ', '.join(site.get('themes', [])),
                            ', '.join([vuln['title'] for vuln in site.get('vulnerabilities', [])]),
                            'Enabled' if site.get('xmlrpc') else 'Disabled',  
                            ', '.join([f"{path[0]} -> {path[1]}" for path in site.get('paths', [])])
                        ])
                print(Fore.GREEN + f"Results saved to {output_file} (CSV format)")

            else:
                
                with open(output_file, 'w') as file:
                    for site in results:
                        file.write(f"\nSite: {site['url']}\n")
                        file.write(f"WordPress: {'Yes' if site['is_wordpress'] else 'No'}\n")
                        if site['version']:
                            file.write(f"Version: {site['version']}\n")
                        if site['users']:
                            file.write(f"Users: {', '.join(site['users'])}\n")
                        if site['plugins']:
                            file.write("Plugins:\n")
                            for plugin in site['plugins']:
                                file.write(f"  - {plugin}\n")
                        if site['themes']:
                            file.write("Themes:\n")
                            for theme in site['themes']:
                                file.write(f"  - {theme}\n")
                        if site.get('vulnerabilities'):
                            file.write("Vulnerabilities:\n")
                            for vuln in site['vulnerabilities']:
                                file.write(f"  - {vuln['title']} (Severity: {vuln['severity']})\n")
                        if site.get('xmlrpc') is not None:  
                            file.write(f"XML-RPC: {'Enabled' if site['xmlrpc'] else 'Disabled'}\n")
                        file.write("Paths:\n")
                        for path in site['paths']:
                            file.write(f"  {path[0]} -> {path[1]}\n")
                print(Fore.GREEN + f"Results saved to {output_file} (Text format)")

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
                plugin_name = path.split('/')[-2]
                print(Fore.GREEN + f"\nFound {resource_type[:-1]}: {plugin_name}")

                
                version = None
                if 'readme.txt' in path:
                    version_match = re.search(r'Stable tag: (\d+\.\d+\.\d+)', response.text)
                    if version_match:
                        version = version_match.group(1)
                        print(Fore.CYAN + f"Version: {version}")

                
                if version:
                    plugin_entry = f"{plugin_name} ({version})"
                else:
                    plugin_entry = plugin_name
                resources.append(plugin_entry)
                print(Fore.YELLOW + f"Debug: Added plugin: {plugin_entry}")  

                
                if version and ('-p' in sys.argv or '--plugins' in sys.argv):
                    vulnerabilities = check_vuln_db(plugin_name, version)
                    if vulnerabilities:
                        print(Fore.RED + f"Vulnerabilities found in {plugin_name} {version}:")
                        for vuln in vulnerabilities:
                            print(Fore.RED + f"  - {vuln['title']} (Severity: {vuln['severity']})")
                    else:
                        print(Fore.GREEN + f"No vulnerabilities found in {plugin_name} {version}")

        except requests.RequestException:
            continue
            
    return resources

#------------------#
#  XML-RPC Check   #
#------------------#
def check_xmlrpc(website):
    if not website.endswith('/'):
        website +='/'
    url = f"{website}xmlrpc.php"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200 and "XML-RPC server accepts POST requests only" in response.text:
            return (True, "XML-RPC enabled (potential security risk)")
        return (False, "XML-RPC not enabled")
    except requests.RequestException:
        return (False, "Error checking XML-RPC")

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

                if '-t' in sys.argv or '--themes' in sys.argv:
                    themes = check_resources(site, 'themes')
                    site_data['themes'] = themes
                
                if '-x' in sys.argv or '--xmlrpc' in sys.argv:
                    xmlrpc_status = check_xmlrpc(site)
                    print(Fore.YELLOW + xmlrpc_status[1])
                    site_data['xmlrpc'] = xmlrpc_status[0]

                print(Fore.BLUE + f"\nChecking paths for {site}...\n")
                paths = handle_site_list('paths.txt')  
                path_results = check_paths(site, paths, get_method_from_args())
                site_data['paths'] = path_results
                
                all_results.append(site_data)

            else:
                print(Fore.RED + emoji.emojize('\n❌ ') + f"No, {site} does not appear to be running WordPress :( .\n")
                all_results.append(site_data)
                continue

            print(Fore.BLUE + f"\nChecking paths for {site}...\n")
            results = check_paths(site, paths, method=get_method_from_args())
            site_data['paths'] = results
            all_results.append(site_data)

    except KeyboardInterrupt:
        print(Fore.RED + "\nProcess terminated by user. Exiting gracefully.")
        save_file(all_results)
        sys.exit(1)

    print(Fore.YELLOW + f"Debug: All Results: {json.dumps(all_results, indent=2)}")

    save_file(all_results)