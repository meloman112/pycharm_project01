import zipfile
import os


def zip_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                absolute_path = os.path.join(root, file)
                relative_path = os.path.relpath(absolute_path, folder_path)
                zipf.write(absolute_path, relative_path)
    return True


folder_to_zip = 'screenshots'
zip_file_path = 'zips/screenshots.zip'

print(zip_folder(folder_to_zip, zip_file_path))



