from zipfile import ZipFile
import os

ROOT_DIR_FILES = [
    '__init__.py',
    'BGTInloopTool.py',
    'BGTInloopTool_dialog.py',
    'BGTInloopTool_dialog_base.ui',
    'icon.png',
    'metadata.txt',
    'ogr2qgis.py',
    'resources.py',
    'resources.qrc'
]

DIRECTORIES = [
    'core',
    'style'
]


def zipdir(path, ziph, path_in_zip):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            zip_file_path = os.path.join(path_in_zip, file_path )
            ziph.write(file_path, zip_file_path)


# create a ZipFile object
try:
    os.remove('bgtinlooptool.zip')
except FileNotFoundError:
    pass
zip = ZipFile('bgtinlooptool.zip', 'w')

# Files in root
for file in ROOT_DIR_FILES:
    zip.write(file, os.path.join('bgtinlooptool', os.path.basename(file)))

# Folders in root
for directory in DIRECTORIES:
    zipdir(directory, zip, 'bgtinlooptool')

# close the Zip File
zip.close()