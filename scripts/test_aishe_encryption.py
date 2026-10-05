import base64
import os
import ssl
import urllib.request
from urllib.parse import quote
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

PASSPHRASE = b"0123456789123456"

def generate_key(salt_bytes):
    # keySize: 4 words = 16 bytes, iterations: 1000, sha1 is default in CryptoJS
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA1(),
        length=16,
        salt=salt_bytes,
        iterations=1000
    )
    return kdf.derive(PASSPHRASE)

def encrypt_value(value_str):
    if not value_str:
        return value_str
    
    # Generate 16 bytes IV and 32 bytes Salt
    iv = os.urandom(16)
    salt = os.urandom(32)
    
    key = generate_key(salt)
    
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(str(value_str).encode("utf-8")) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    iv_hex = iv.hex()
    salt_hex = salt.hex()
    ct_b64 = base64.b64encode(ciphertext).decode("utf-8")
    
    combined = f"{iv_hex}::{salt_hex}::{ct_b64}"
    return base64.b64encode(combined.encode("utf-8")).decode("utf-8")

def decrypt_value(enc_b64):
    if not enc_b64:
        return enc_b64
    try:
        combined = base64.b64decode(enc_b64).decode("utf-8")
        parts = combined.split("::")
        if len(parts) != 3:
            return enc_b64
        iv = bytes.fromhex(parts[0])
        salt = bytes.fromhex(parts[1])
        ciphertext = base64.b64decode(parts[2])
        
        key = generate_key(salt)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        
        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()
        return data.decode("utf-8")
    except Exception as e:
        return f"DecryptError: {e}"

# Test self-encryption / decryption
test_val = "Madhya Pradesh"
enc = encrypt_value(test_val)
dec = decrypt_value(enc)
print(f"Self-test: original='{test_val}', decrypted='{dec}', match={test_val == dec}")

# Now test calling AISHE API with encrypted parameters!
survey_year_enc = encrypt_value("2020") # or 2022/2024
state_enc = encrypt_value("23") # MP state code is 23

urls_to_try = [
    # With space (encoded as %20)
    f"https://pdf.aishe.nic.in/aisheinstitutemanagement/institutionDirectory%20/getUniversityList?stateCode={quote(state_enc)}&surveyYear={quote(survey_year_enc)}",
    # Without space
    f"https://pdf.aishe.nic.in/aisheinstitutemanagement/institutionDirectory/getUniversityList?stateCode={quote(state_enc)}&surveyYear={quote(survey_year_enc)}",
    # Unencrypted parameters just in case
    "https://pdf.aishe.nic.in/aisheinstitutemanagement/institutionDirectory/getUniversityList?stateCode=23&surveyYear=2020",
    "https://pdf.aishe.nic.in/aisheinstitutemanagement/institutionDirectory%20/getUniversityList?stateCode=23&surveyYear=2020",
    # Search API
    f"https://pdf.aishe.nic.in/aisheinstitutemanagement/apis/search-institute-by-aishe-or-name?searchText=Guna&surveyYear=2020",
    f"https://pdf.aishe.nic.in/aisheinstitutemanagement/apis/search-institute-by-aishe-or-name?searchText={quote(encrypt_value('Guna'))}&surveyYear=2020"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://dashboard.aishe.gov.in",
    "Referer": "https://dashboard.aishe.gov.in/"
}

for u in urls_to_try:
    print(f"\nRequesting: {u[:110]}...")
    req = urllib.request.Request(u, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=12) as resp:
            content = resp.read().decode("utf-8")
            print(f"SUCCESS -> Status: {resp.status} | Length: {len(content)}")
            print("Preview:", content[:300])
            # If the response is a string, check if it's encrypted
            if len(content) < 500 and "::" in content or (content.startswith('"') and len(content) > 30):
                unquoted = content.strip('"')
                decrypted = decrypt_value(unquoted)
                print("Decrypted preview:", decrypted[:300])
    except Exception as e:
        print(f"FAILED -> {e}")
