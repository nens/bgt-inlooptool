from zipfile import ZipFile
from typing import List
import os
from distutils.dir_util import copy_tree, remove_tree

ROOT_DIR_FILES = [
    "__init__.py",
    "BGTInloopTool.py",
    "BGTInloopTool_dialog.py",
    "BGTInloopTool_dialog_base.ui",
    "constants.py",
    "icon.png",
    "metadata.txt",
    "LICENSE"
    "ogr2qgis.py",
    "resources.py",
    "resources.qrc",
]

DIRECTORIES = ["core", "style", "processing", "utils"]

IGNORE = ["core/__pycache__", "core/.gitignore"]


def zipdir(path, zipfile_handle, path_in_zip, ignore: List = None):
    if ignore is not None:
        ignore_normpath = [os.path.normpath(path_str) for path_str in ignore]
    for root, dirs, files in os.walk(path):
        if root not in ignore_normpath:
            for file_name in files:
                if file_name not in ignore_normpath:
                    file_path = os.path.join(root, file_name)
                    zip_file_path = os.path.join(path_in_zip, file_path)
                    zipfile_handle.write(file_path, zip_file_path)


# Copy core to bgtinlooptool
try:
    remove_tree("core")
except FileNotFoundError:
    pass
copy_tree("../../core", "core")

# create a ZipFile object
try:
    os.remove("bgtinlooptool.zip")
except FileNotFoundError:
    pass
tgt_zip = ZipFile("bgtinlooptool.zip", "w")

# Files in root
for file in ROOT_DIR_FILES:
    tgt_zip.write(file, os.path.join("bgtinlooptool", os.path.basename(file)))

# Folders in root
for directory in DIRECTORIES:
    zipdir(
        path=directory,
        zipfile_handle=tgt_zip,
        path_in_zip="bgtinlooptool",
        ignore=IGNORE,
    )

# close the Zip File
tgt_zip.close()

# clean up
try:
    remove_tree("core")
except FileNotFoundError:
    pass
