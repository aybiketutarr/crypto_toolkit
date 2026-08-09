                             ██████╗ ██████╗ ██╗   ██╗██████╗ ████████╗ ██████╗_TOOLKIT_
                             ██╔════╝ ██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔═══██╗
                             ██║      ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ██║   ██║
                             ██║      ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██║   ██║
                             ╚██████╗ ██║  ██║   ██║   ██║        ██║   ╚██████╔╝
                              ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝    ╚═════╝
                                          Secure Cryptography Toolkit




## Purpose
Data security is a critical necessity in today's digital environment. By consolidating fundamental cryptographic operations into a menu-driven or single command-line interface, this toolkit offers a range of capabilities, including secure file processing, message protection, integrity verification, and the storage of sensitive data.  

Professional objectives of the toolkit:  
- **Applied Security**: Implements industry-standard algorithms such as AES-GCM and RSA for file and message protection.  
- **Integrity Assurance**: Provides SHA256 hashing and signature verification to ensure data has not been altered.  
- **Authentication**: Uses RSA signing and verification to confirm the authenticity of files and sources.  
- **Confidentiality**: Offers steganography to conceal information within PNG images for an additional security layer.  
- **Educational Use**: Serves as a practical tool for students and researchers to experiment with cryptographic concepts.  

This toolkit is designed for both **cybersecurity professionals** and **academic/research environments**.

---

![OVERVİEW](Overview.png)


## Features
- AES-GCM file encryption/decryption  
- RSA key generation, message encryption/decryption  
- RSA file signing and signature verification  
- SHA256 hashing and integrity checks  
- Strong password generation  
- Steganography for hiding/extracting data in PNG images  
- ASCII menu interface with quick reply
- Command-line argument support → Run specific operations directly with flags (e.g., --encrypt, --manual, --password) without using the interactive menu.



---

## 📦 Installation and usage

You can use the tool **interactively via the menu** or run it directly from the command line using **arguments**.

> ⚠️ **Note:** Due to modern system restrictions (such as externally-managed environments), you must utilize the virtual environment (`venv`) to ensure external libraries function correctly.

---

### İnteractive Menu Mode
```bash
git clone https://github.com/aybiketutarr/crypto_toolkit.git
cd crypto_toolkit
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python crypto.py
```


### Command-Line Arguments Mode
* **Method 1: Activating the virtual environment first (Recommended)**
  > *Note: To use this method, you must be in the project's root folder (`cd crypto_toolkit`) in the terminal.*
  ```bash
  source venv/bin/activate
  python crypto.py --encrypt ~/file.txt

* **Method 2: Directly via the venv Python path (Without entering the folder)**
 ```bash
/path/to/your/crypto_toolkit/venv/bin/python /path/to/your/crypto_toolkit/crypto.py --encrypt ~/file.txt
