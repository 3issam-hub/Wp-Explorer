![Wp-Explorer-logo](/assets/logo.png)
# **Wp-Explorer**

<p>
  Wp-Explorer is a Python-based tool designed to explore WordPress websites for sensitive paths and endpoints. It checks the response status codes for
  these paths, allowing you to identify potential issues or points of interest. Wp-Explorer supports both GET and POST HTTP methods for its requests.
</p>

## Features

- Detects if a website is running WordPress.
- Scans sensitive WordPress paths and endpoints.
- Outputs status codes for scanned paths (e.g., 200, 404, etc.).
- Allows saving results to a file.
- Supports GET and POST HTTP methods.
- Graceful handling of network errors and interruptions.
- etc..


## 🛠️ Installation

<br>

```bash
git clone https://github.com/3issam-hub/Wp-Explorer.git
cd Wp-Explorer
pip install -r requirements.txt
python3 Wp-Explorer https://example.com/
```

<br>

> Ensure a file named paths.txt is in the same directory. This file should contain the paths you want to check (one path per line).


 

## ⚙️Usage

Run the script with the following syntax:

`python3 Wp-Explorer.py [Website] [Options]`

### Arguments

Website: The URL of the target WordPress site (e.g., http://example.com).


### Options

-h,--help:Display the help menu.

-o <filename>,--output-file <filename>:Save the results to a specified file.

-m <method>,--method <method>:Specify the HTTP method to use (GET or POST). Defaults to GET.


## 📚 CLI Example

### Basic Scan:

`python3 Wp-Explorer.py http://example.com`

### Scan with POST Method:

`python3 Wp-Explorer.py http://example.com -m POST`

### Save Results to File:

`python3 Wp-Explorer.py http://example.com -o results.txt`

### Display Help:

`python3 Wp-Explorer.py -h`


 

## How It Works

1. WordPress Detection:

The tool checks for key WordPress-specific paths **(wp-login.php, wp-admin/, wp-content/)** to verify if the target website is running WordPress.


2. Path Scanning:

  Reads paths from paths.txt and sends HTTP requests to the target website.
  Outputs the status code for each path:

    - 200: Path exists.
    - 404: Path does not exist.
    - Other codes (e.g., 403, 401): Restricted access or errors.

3. Saving Results:

If specified with -o, results are saved to the provided filename.


### 📝 License

This project is licensed under the **[MIT License](https://github.com/aws/mit-0)**.

### Contribution

Contributions are welcome! Feel free to open an issue or submit a pull request.

>⚠️ Disclaimer
>
>This tool is intended for educational and ethical purposes only. Ensure you have proper authorization before scanning any website. Misuse of this tool may result in legal consequences. Use responsibly.

## Author

**Issam Beniysa**
Feel free to connect with **[me](https://issambeniysa.site)** for suggestions or questions!
