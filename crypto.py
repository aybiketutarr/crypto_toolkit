import argparse
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import hashlib, os, secrets, string, hmac, datetime
from PIL import Image
from PIL import PngImagePlugin

# === ASCII Bannerlar ===
def opening_banner():
    print("\033[95m")
    print(r"""
  ██████╗ ██████╗ ██╗   ██╗██████╗ ████████╗ ██████╗_TOOLKIT_
 ██╔════╝ ██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔═══██╗
 ██║      ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ██║   ██║
 ██║      ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██║   ██║
 ╚██████╗ ██║  ██║   ██║   ██║        ██║   ╚██████╔╝
  ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝    ╚═════╝
    """)
    print("\033[0m")

def closing_banner():
    print("\033[95m")
    print(r"""
_.-'''''-._
.'  _HACKER_  '.
|  [_] [__]   |   SYSTEM OFFLINE.
|  [===]      |   ENCRYPTION KEYS SECURED.
'.___________.'   GOODBYE.
     |   |
     |___|
    """)
    print("\033[0m")
    print("Goodbye! Thanks for using Secure Cryptography Toolkit.")



def show_help():
    print("""
=== Cryptography Toolkit - Help ===

[+] 1 → AES-GCM Encrypt
    Encrypt a file with AES-GCM
    Usage: Enter filename → outputs filename.enc

[+] 2 → AES-GCM Decrypt
    Decrypt a file with AES-GCM
    Usage: Enter .enc file → outputs filename.dec

[+] 3 → Generate RSA Keys
    Generate RSA key pair (private.pem & public.pem)

[+] 4 → RSA Encrypt
    Encrypt a message using public.pem
    Usage: Input message → outputs message.enc

[+] 5 → RSA Decrypt
    Decrypt message.enc using private.pem

[+] 6 → File Hash
    Calculate SHA256 hash of a file

[+] 7 → Generate AES Key
    Generate a 32-byte AES key (aes.key)

[+] 8 → Verify File Hash
    Compare file hash with expected value

[+] 9 → Strong Password
    Generate a random strong password
    Usage: Input length → outputs password

[+] 10 → View Logs
    Display logs.txt contents

[+] 11 → RSA Sign
    Sign a file with private.pem
    Usage: Input filename → outputs filename.sig

[+] 12 → RSA Verify
    Verify file signature with public.pem

[+] 13 → Steg Hide
    Hide a secret file inside a PNG image
    Usage: Input PNG + secret file → outputs steg.png

[+] 14 → Steg Extract
    Extract hidden data from a PNG image
    Usage: Input steg.png + output file

[+] 15 → Quit
    Exit the program

--- CLI Usage Examples ---
python toolkit1.py --encrypt file.txt
python toolkit1.py --decrypt file.txt.enc
python toolkit1.py --rsa-encrypt "Message"
python toolkit1.py --rsa-decrypt message.enc
python toolkit1.py --hash file.txt
python toolkit1.py --password 16
python toolkit1.py --steg-hide image.png secret.txt
python toolkit1.py --steg-extract steg.png output.txt
python toolkit.py --manual (help menu)
""")



# === Loglama ===
def log_action(action, details=""):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("logs.txt", "a") as log_file:
        log_file.write(f"[{timestamp}] {action} - {details}\n")

# === AES-GCM Şifreleme ===
def encrypt_file(filename, key):
    cipher = AES.new(key, AES.MODE_GCM)
    plaintext = open(filename, 'rb').read()
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    with open(filename + ".enc", 'wb') as f:
        f.write(cipher.nonce + tag + ciphertext)
    print(f"[\033[95m+\033[0m] {filename} encrypted → {filename}.enc")
    log_action("Encrypt File", filename)

def decrypt_file(filename, key):
    data = open(filename, 'rb').read()
    nonce, tag, ciphertext = data[:16], data[16:32], data[32:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    with open(filename.replace(".enc", ".dec"), 'wb') as f:
        f.write(plaintext)
    print(f"[\033[95m+\033[0m] {filename} decrypted → {filename.replace('.enc','.dec')}")
    log_action("Decrypt File", filename)

# === RSA Anahtar Yönetimi ===
def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key(passphrase="StrongPass123!", pkcs=8, protection="scryptAndAES128-CBC")
    public_key = key.publickey().export_key()
    open("private.pem","wb").write(private_key)
    open("public.pem","wb").write(public_key)
    print("[\033[95m+\033[0m] RSA keys generated (protected).")
    log_action("Generate RSA Keys","private.pem & public.pem")

def rsa_encrypt(message, pubkey_file="public.pem"):
    pubkey = RSA.import_key(open(pubkey_file,"rb").read())
    cipher = PKCS1_OAEP.new(pubkey)
    ciphertext = cipher.encrypt(message.encode())
    open("message.enc","wb").write(ciphertext)
    print("[\033[95m+\033[0m] Message encrypted → message.enc")
    log_action("RSA Encrypt","message.enc")

def rsa_decrypt(enc_file="message.enc", privkey_file="private.pem"):
    privkey = RSA.import_key(open(privkey_file,"rb").read(), passphrase="StrongPass123!")
    cipher = PKCS1_OAEP.new(privkey)
    ciphertext = open(enc_file,"rb").read()
    message = cipher.decrypt(ciphertext)
    print("[\033[95m+\033[0m] Message decrypted:", message.decode())
    log_action("RSA Decrypt", enc_file)

# === RSA İmza / Doğrulama ===
def sign_file(filename, privkey_file="private.pem"):
    privkey = RSA.import_key(open(privkey_file,"rb").read(), passphrase="StrongPass123!")
    data = open(filename,"rb").read()
    h = SHA256.new(data)   # hashlib yerine Crypto.Hash.SHA256 kullanılıyor
    signature = pkcs1_15.new(privkey).sign(h)
    open(filename+".sig","wb").write(signature)
    print(f"[\033[95m+\033[0m File signed → {filename}.sig")
    log_action("Sign File", filename)

def verify_signature(filename, sig_file, pubkey_file="public.pem"):
    pubkey = RSA.import_key(open(pubkey_file,"rb").read())
    data = open(filename,"rb").read()
    h = SHA256.new(data)   # hashlib yerine Crypto.Hash.SHA256
    signature = open(sig_file,"rb").read()
    try:
        pkcs1_15.new(pubkey).verify(h, signature)
        print("[\033[95m+\033[0m] Signature verified successfully.")
        log_action("Verify Signature", filename)
    except (ValueError, TypeError):
        print("[\033[95m!\033[0m] Signature verification failed.")
        log_action("Verify Signature Failed", filename)

# === Steganografi ===
def steg_hide(image_file, secret_file, output_file="steg.png"):
    img = Image.open(image_file)
    data = open(secret_file,"rb").read()
    info = PngImagePlugin.PngInfo()
    info.add_text("secret", data.hex())
    img.save(output_file, "PNG", pnginfo=info)
    print(f"[\033[95m+\033[0m] Secret hidden in {output_file}")
    log_action("Steg Hide", secret_file)

def steg_extract(image_file, output_file="extracted.txt"):
    img = Image.open(image_file)
    if "secret" in img.text:   # Burada img.info yerine img.text kullanılmalı
        data = bytes.fromhex(img.text["secret"])
        with open(output_file, "wb") as f:
            f.write(data)
        print(f"[\033[95m+\033[0m] Secret extracted → {output_file}")
        log_action("Steg Extract", image_file)
    else:
        print("[\033[95m!\033[0m] No hidden data found.")


# === AES Key Generation ===
def generate_aes_key():
    key = get_random_bytes(32)
    open("aes.key","wb").write(key)
    os.chmod("aes.key",0o600)
    print("[\033[95m+\033[0m] AES key generated → aes.key")
    log_action("Generate AES Key","aes.key")

# === Hashing ===
def hash_file(filename, algorithm="sha256"):
    h = hashlib.new(algorithm)
    with open(filename,"rb") as f:
        while chunk := f.read(4096):
            h.update(chunk)
    print(f"[\033[95m+\033[0m] {filename} {algorithm} hash: {h.hexdigest()}")
    log_action("Hash File", filename)

def verify_file_hash(filename, expected_hash, algorithm="sha256"):
    h = hashlib.new(algorithm)
    with open(filename,"rb") as f:
        while chunk := f.read(4096):
            h.update(chunk)
    actual_hash = h.hexdigest()
    if hmac.compare_digest(actual_hash, expected_hash):
        print(f"[\033[95m+\033[0m] Hash verified successfully for {filename}")
    else:
        print(f"[\033[95m!\033[0m] Hash mismatch! Expected {expected_hash}, got {actual_hash}")

# === Password Generator ===
def generate_strong_password(length=16, include_special=True):
    if length < 12:
        print("[\033[95m!\033[0m] Minimum length is 12.")
        return
    alphabet = string.ascii_letters + string.digits
    if include_special:
        alphabet += string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    print(f"[\033[95m+\033[0m] Strong password: {password}")
    log_action("Generate Password", f"Length {length}")


# === Argüman desteği ===
def parse_args():
    parser = argparse.ArgumentParser(description="Secure Cryptography Toolkit")

    # 0) Help
    parser.add_argument("--manual", action="store_true", help="Show custom help menu")

    # 1) AES-GCM Encrypt
    parser.add_argument("--encrypt", help="Encrypt a file with AES-GCM")

    # 2) AES-GCM Decrypt
    parser.add_argument("--decrypt", help="Decrypt a file with AES-GCM")

    # 3) RSA Keys
    parser.add_argument("--rsa-keys", action="store_true", help="Generate RSA key pair")

    # 4) RSA Encrypt
    parser.add_argument("--rsa-encrypt", help="Encrypt a message with RSA")

    # 5) RSA Decrypt
    parser.add_argument("--rsa-decrypt", help="Decrypt a message file with RSA")

    # 6) File Hash
    parser.add_argument("--hash", help="Calculate SHA256 hash of a file")

    # 7) AES Key
    parser.add_argument("--aes-key", action="store_true", help="Generate AES key")

    # 8) Verify Hash
    parser.add_argument("--verify-hash", nargs=2, help="Verify file hash (file, expected_hash)")

    # 9) Strong Password
    parser.add_argument("--password", type=int, help="Generate strong password of given length")

    # 10) View Logs
    parser.add_argument("--logs", action="store_true", help="View logs")

    # 11) RSA Sign
    parser.add_argument("--rsa-sign", help="Sign a file with RSA")

    # 12) RSA Verify
    parser.add_argument("--rsa-verify", nargs=2, help="Verify RSA signature (file, sig_file)")

    # 13) Steg Hide
    parser.add_argument("--steg-hide", nargs=2, help="Hide secret in PNG (image, secret)")

    # 14) Steg Extract
    parser.add_argument("--steg-extract", nargs=2, help="Extract secret from PNG (image, output)")

    return parser.parse_args()




# === Menü ===
def main():
    opening_banner()
    print("=== Cryptography Toolkit ===")
    print("""
    0) help
    1) Encrypt file(s) with AES-GCM
    2) Decrypt file(s) with AES-GCM
    3) Generate RSA keys
    4) Encrypt message with RSA
    5) Decrypt message with RSA
    6) Calculate file hash
    7) Generate AES key
    8) Verify file hash
    9) Generate strong password
    10) View logs
    11) Sign file with RSA
    12) Verify RSA signature
    13) Hide secret in image (Steganografi)
    14) Extract secret from image (Steganografi)
    15) Quit
    """)

    while True:
        choice = input("Select an option: ")

        if choice == "1":
            key = get_random_bytes(32)
            filename = input("File name: ")
            encrypt_file(filename, key)
            open("aes.key","wb").write(key)

        elif choice == "2":
            key = open("aes.key","rb").read()
            filename = input("Encrypted file name: ")
            decrypt_file(filename, key)

        elif choice == "3":
            generate_rsa_keys()

        elif choice == "4":
            msg = input("Message: ")
            rsa_encrypt(msg, "public.pem")

        elif choice == "5":
            rsa_decrypt("message.enc", "private.pem")

        elif choice == "6":
            filename = input("File name: ")
            hash_file(filename)

        elif choice == "7":
            generate_aes_key()

        elif choice == "8":
            filename = input("File name: ")
            expected = input("Expected hash: ")
            verify_file_hash(filename, expected)

        elif choice == "9":
            length = int(input("Password length (default 16): ") or 16)
            generate_strong_password(length)

        elif choice == "10":
            print(open("logs.txt").read() if os.path.exists("logs.txt") else "[!] No logs yet.")

        elif choice == "11":
            filename = input("File to sign: ")
            sign_file(filename)

        elif choice == "12":
            filename = input("File to verify: ")
            sigfile = input("Signature file: ")
            verify_signature(filename, sigfile)

        elif choice == "13":
            image = input("Image file (PNG): ")
            secret = input("Secret file to hide: ")
            steg_hide(image, secret)

        elif choice == "14":
            image = input("Image file (PNG): ")
            output = input("Output file name: ")
            steg_extract(image, output)

        elif choice == "0":
            show_help()

        elif choice == "15":
            closing_banner()
            break

        else:
            print("Invalid choice!")



if __name__ == "__main__":
    args = parse_args()

     # Eğer kullanıcı --help yazdıysa, menüye girmeden yardım göster
    if args.manual:
        show_help()
        exit(0)   # programı bitiriyoruz

    if args.encrypt:
        key = get_random_bytes(32)
        encrypt_file(args.encrypt, key)
        open("aes.key","wb").write(key)

    elif args.decrypt:
        key = open("aes.key","rb").read()
        decrypt_file(args.decrypt, key)

    elif args.rsa_encrypt:
        rsa_encrypt(args.rsa_encrypt, "/home/hacker/Desktop/crypto_toolkit/public.pem")

    elif args.rsa_decrypt:
         rsa_decrypt(args.rsa_decrypt, "/home/hacker/Desktop/crypto_toolkit/private.pem")

    elif args.hash:
        hash_file(args.hash)

    elif args.password:
        generate_strong_password(args.password)

    elif args.steg_hide:
        steg_hide(args.steg_hide[0], args.steg_hide[1])

    elif args.steg_extract:
        steg_extract(args.steg_extract[0], args.steg_extract[1])

    else:
        main()  # Eğer argüman yoksa menüye gir
