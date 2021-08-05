from zipfile import ZipFile
from typing import List
import os

ROOT_DIR_FILES = [
    '__init__.py',
    'BGTInloopTool.py',
    'BGTInloopTool_dialog.py',
    'BGTInloopTool_dialog_base.ui',
    'dependencies.py',
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

IGNORE = [
    'core/__pycache__',
    'core/.gitignore'
]


def zipdir(path, ziph, path_in_zip, ignore: List = None):
    # ziph is zipfile handle
    if ignore is None:
        ignore = list()
    else:
        ignore_normpath = [os.path.normpath(path_str) for path_str in ignore]
    for root, dirs, files in os.walk(path):
        if root not in ignore_normpath:
            for file_name in files:
                if file_name not in ignore_normpath:
                    file_path = os.path.join(root, file_name)
                    zip_file_path = os.path.join(path_in_zip, file_path)
                    ziph.write(file_path, zip_file_path)


# create a ZipFile object
try:
    os.remove('bgtinlooptool.zip')
except FileNotFoundError:
    pass
tgt_zip = ZipFile('bgtinlooptool.zip', 'w')

# Files in root
for file in ROOT_DIR_FILES:
    tgt_zip.write(file, os.path.join('bgtinlooptool', os.path.basename(file)))

# Folders in root
for directory in DIRECTORIES:
    zipdir(directory, tgt_zip, 'bgtinlooptool', ignore=IGNORE)

# close the Zip File
tgt_zip.close()
