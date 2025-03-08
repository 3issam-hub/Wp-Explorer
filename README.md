![Wp-Explorer-logo](/assets/logo.png)
# **Wp-Explorer**

<p>
  Wp-Explorer is a Python-based tool designed to explore WordPress websites for sensitive paths and endpoints. It checks the response status codes for
  these paths, allowing you to identify potential issues or points of interest. Wp-Explorer supports both GET and POST HTTP methods for its requests.
</p>

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)
![Open Source](https://img.shields.io/badge/Open%20Source-%E2%9D%A4-red)

## Features

- ✅ WordPress detection with multiple verification methods
- 🔍 Scans sensitive paths from `paths.txt` with status code analysis
- 📜 Identifies WordPress version through metadata/readme files
- 👥 User account enumeration via author ID probing
- 🧩 Plugin/Themes detection using `plugins.txt` and `themes.txt`
- 🚨 Vulnerability checks using WPScan Vulnerability Database
- 📡 XML-RPC endpoint status verification
- 📂 Multi-site scanning from a file input
- 🎨 Color-coded console output with ASCII art
- ⚡ Configurable delays between requests
- 📊 Export results to text/JSON/CSV formats

## 📋 Requirements

- Python 3.7 or higher
- Required files in root directory:
  - `paths.txt` - Contains paths to scan
  - `plugins.txt` - Common plugin paths
  - `themes.txt` - Common theme paths
- Optional `config.ini` for API keys and settings

## 🚀 Quick Start

### ⚒️ Installation

```bash
# Clone repository
git clone https://github.com/3issam-hub/Wp-Explorer.git
cd Wp-Explorer

# Install dependencies
pip install -r requirements.txt

# Create necessary files
touch paths.txt plugins.txt themes.txt
```

> Populate `paths.txt`, `plugins.txt`, and `themes.txt` with paths (one per line)

### ⚙️ Configuration

modify `config.ini` to customize settings:

```ini
[Api]
api_key = your_wpscan_api_key  # Required for vulnerability checks

[Settings]
max_users_to_check = 10
request_delay = 1
output_format = text  # Options: text, json, csv
```

### 🖥️ Usage

**Basic Command:**
```bash
python3 Wp-Explorer.py <URL> [OPTIONS]
```

#### Options
| Flag | Description |
|------|-------------|
| `-h`, `--help`       | Show help message |
| `-o FILE`, `--output FILE` | Save results to file (supports .txt, .json, .csv) |
| `-m METHOD`, `--method METHOD` | HTTP method: GET (default) or POST |
| `-l FILE`, `--site-list FILE` | Scan multiple sites from file |
| `-v`, `--version`    | Detect WordPress version |
| `-u`, `--users`      | Enumerate user accounts |
| `-p`, `--plugins`    | Check for installed plugins |
| `-t`, `--themes`     | Check for installed themes |
| `-x`, `--xmlrpc`     | Verify XML-RPC status |
| `--delay SECONDS`    | Set delay between requests (default: 1s) |

### 📚 Examples

1. **Basic Scan with JSON Output**
```bash
python3 Wp-Explorer.py http://example.com -v -u -o results.json
```

2. **Multi-Site Plugin Check**
```bash
python3 Wp-Explorer.py -l targets.txt -p --delay 2
```

3. **Full Security Audit**
```bash
python3 Wp-Explorer.py http://example.com -vuptx -m POST -o audit.csv
```

## 🔍 How It Works

1. **WordPress Verification**  
   Checks for `wp-login.php`, `wp-admin/`, and `wp-content/` paths.

2. **Version Detection**  
   Scans HTML meta tags, readme files, and RSS feeds for version information.

3. **User Enumeration**  
   Tests `?author={ID}` endpoints to discover valid usernames.

4. **Plugin/Theme Detection**  
   Checks paths from `plugins.txt` and `themes.txt` for 200 responses.

5. **Vulnerability Assessment**  
   Uses WPScan API to check for known vulnerabilities in detected components.

6. **XML-RPC Check**  
   Verifies if XML-RPC interface is enabled (potential security risk).

## 🤝 Contribution

Contributions welcome! Follow these steps:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open Pull Request

## 📜 License

This project is licensed under the **GNU General Public License v3.0** - see [LICENSE](https://www.gnu.org/licenses/gpl-3.0) for details.

## ⚠️ Disclaimer

> This tool is intended for **authorized security testing** and **educational purposes only**. Unauthorized use against websites without explicit permission is illegal. The developers assume no liability for misuse of this software.

---

<p align="center">
  Made with ♥️ by Issam Beniysa<br>
  <a href="https://issambeniysa.site">Contact Me</a> | 
  <a href="https://github.com/3issam-hub/Wp-Explorer/issues">Report Issue</a>
</p>
