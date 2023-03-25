"""
Description:
A script that downloads and silently runs
a VLC media player installer file, verified by
hash values. The installer file is discarded after use.

Usage:
python lab6.py

"""

import requests as rq
import hashlib
import os
import subprocess

def main():

    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256()
    
    # Download (but don't save) the VLC installer from the VLC website
    installer_data = download_installer()

    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values
    if installer_ok(installer_data, expected_sha256):

        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)

        # Silently run the VLC installer
        run_installer(installer_path)

        # Delete the VLC installer from disk
        delete_installer(installer_path)

def get_expected_sha256():
    """
    Fetches the expected hash value from the videolan website

    Returns:
        str: the expected SHA256 hash of the installer file
    """    

    file_url = 'http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe.sha256'
    resp_msg = rq.get(file_url)

    if resp_msg.status_code == rq.codes.ok:

        file_content = resp_msg.text
        hash = file_content.split(" ")[0]

    return hash

def download_installer():
    """
    Downloads the VLC installer and returns the data of the installer

    Returns:
        byte str: The binary data of the installer file
    """    
    
    file_url = 'http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe'
    resp_msg = rq.get(file_url)

    if resp_msg.status_code == rq.codes.ok:
        return resp_msg.content

    return

def installer_ok(installer_data, expected_sha256):
    """
    Checks that the hash value of the downloaded file
    matches the expected hash value provided by the VLC website.

    Args:
        installer_data (byte str): The binary data of the installer file
        expected_sha256 (str): The expected hash value of the installer file

    Returns:
        bool: True/False indicator if the hash values match
    """    
    
    installer_hash = hashlib.sha256(installer_data).hexdigest()

    if installer_hash == expected_sha256:
        return True
    
    return False

def save_installer(installer_data):
    """
    Writes the binary data of the installer executable to a file
    and returns the path of the file.

    Args:
        installer_data (byte str): The binary data of the installer

    Returns:
        str: The path of the installer file
    """    

    with open(os.getenv('TEMP')+'\\vlc_installer.exe', 'wb') as file:
        file.write(installer_data)

    return file.name

def run_installer(installer_path):
    """
    Silently runs the installer executable file.

    Args:
        installer_path (str): The path of the installer file
    """    

    subprocess.run([installer_path, '/L=1033', '/S'])

    return
    
def delete_installer(installer_path):
    """
    Deletes the installer executable file

    Args:
        installer_path (str): The path of the installer
    """    

    os.remove(installer_path)
    
    return

if __name__ == '__main__':
    main()