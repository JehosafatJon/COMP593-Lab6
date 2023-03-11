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
    """ Requests the expected hash value for the installer from 
        the VLC website and returns the expected hash value.

    Returns:
        (str): The expected hash value of the vlc installer
    """

    file_url = 'http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe.sha256'
    resp_msg = rq.get(file_url)

    if resp_msg.status_code == rq.codes.ok:

        file_content = resp_msg.text
        hash = file_content.split(" ")[0]

    return hash

def download_installer():
    """ Requests the executable for the installer from 
        the VLC website and returns the binary data
        of the installer.

    Returns:
        (byte str): The installer executable file data
    """

    file_url = 'http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe'
    resp_msg = rq.get(file_url)

    if resp_msg.status_code == rq.codes.ok:
        return resp_msg.content

    return

def installer_ok(installer_data, expected_sha256):
    """ Compares the expected hash value of the installer file
        data to the calculated hash value of the installer file data.

    Args:
        installer_data (byte str): The binary data of the installer executable
        expected_sha256 (str): The expected SHA256 hash value

    Returns:
        (bool): True if expected and calculated hashes match
    """

    installer_hash = hashlib.sha256(installer_data).hexdigest()

    if installer_hash == expected_sha256:
        return True
    
    return False

def save_installer(installer_data):
    """ Writes the installer data to a temporary executable file
        and returns the file path of the new executable file.

    Args:
        installer_data (byte str): the byte data of the executable file

    Returns:
        (str): The file path of the installer .exe file
    """

    with open(os.getenv('TEMP')+'\\vlc_installer.exe', 'wb') as file:
        file.write(installer_data)

    return file.name

def run_installer(installer_path):
    """ Silently runs the installer.

    Args:
        installer_path (str): The path of the installer
    """

    subprocess.run([installer_path, '/L=1033', '/S'])

    return
    
def delete_installer(installer_path):
    """ Deletes the the installer file.

    Args:
        installer_path (str): The path of the installer
    """

    os.remove(installer_path)
    
    return

if __name__ == '__main__':
    main()