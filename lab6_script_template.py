
import requests as rq
import hashlib
import re
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
    file_url = 'http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe.sha256'
    resp_msg = rq.get(file_url)

    if resp_msg.status_code == rq.codes.ok:

        file_content = resp_msg.text
        hash = re.match(r'^(.*) ', file_content).groups(1)[0]

    return hash

def download_installer():
    file_url = 'http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe'
    resp_msg = rq.get(file_url)

    if resp_msg.status_code == rq.codes.ok:
        return resp_msg.content


    return

def installer_ok(installer_data, expected_sha256):
    installer_hash = hashlib.sha256(installer_data).hexdigest()

    if installer_hash == expected_sha256:
        return True
    
    return False

def save_installer(installer_data):
    with open(os.getenv('TEMP')+'\\vlc_installer.exe', 'wb') as file:
        file.write(installer_data)

    return file.name

def run_installer(installer_path):

    subprocess.run([installer_path, '/L=1033', '/S'])

    return
    
def delete_installer(installer_path):
    os.remove(installer_path)
    return

if __name__ == '__main__':
    main()