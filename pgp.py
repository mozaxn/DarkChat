# Importing necessary libraries
import gnupg
import os

def find_priv_key(file, passphrase):
    """Read the PRIVATE KEY from the file passed by the user."""
    
    # Initialize GPG
    gpg = gnupg.GPG()
    
    # Reading the armored key
    try:
        armored = open(file, "r").read()
    
    except:
        return False
    
    # Import into the GPG keyring
    try:
        import_result = gpg.import_keys(armored)
        secret_keys = gpg.list_keys(secret=True)
        fingerprint = secret_keys[-1].get("fingerprint")
        
        exported_key = gpg.export_keys(fingerprint, secret=True, passphrase=passphrase)
        return [fingerprint, exported_key]
    
    except:
        return False
    
def create_pgp(name, email, comment='', passphrase=''):
    gpg = gnupg.GPG() 

    # create key input; adjust params as desired
    key_input = gpg.gen_key_input(
        name_real=name,
        name_email=email,
        name_comment=comment if comment else None,
        key_length=2048,
        expire_date=0,        # or "0" for no expiry
        passphrase=passphrase or None
    )

    key = gpg.gen_key(key_input)

    if not key or not key.fingerprint:
        return False

    fp = key.fingerprint


    if not os.path.isdir("DarkChat"):
        os.mkdir("DarkChat")
    
    # export public key
    pub_armored = gpg.export_keys(fp)
    with open(f"DarkChat/{name}_PUBLIC.asc", "w") as f:
        f.write(pub_armored)
    
    # export private key (armored)
    priv_armored = gpg.export_keys(fp, secret=True, passphrase=passphrase or '')
    with open(f"DarkChat/{name}_PRIVATE.asc", "w") as f:
        f.write(priv_armored)
    
    return fp