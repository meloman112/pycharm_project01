import os
import shutil
import requests

def archive_and_send( url='https://face2.cake-bumer.uz/api/upload-zip'):

     archive_path = 'screenshots/group-2_ID-1.zip'
     with open(archive_path, 'rb') as f:
        files = {'zip_file': (os.path.basename(archive_path), f)}
        response = requests.post(url, files=files)
        print(response.text)

if __name__ == '__main__':
    archive_and_send()