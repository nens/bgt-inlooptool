# https://stackoverflow.com/questions/12332975/installing-python-module-within-code
import subprocess
import sys
import os


def try_install_gdal():

    try:
        import gdal
    except ImportError:
        print("gdal is not installed, trying to install gdal")
        # subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        current_folder = os.path.dirname(__file__)
        wheel = os.path.join(current_folder, 'GDAL-2.2.4-cp27-cp27m-win32.whl')
        subprocess.check_call([sys.executable, "-m", "pip", "install", wheel])
        print("gdal is succesfully installed")
    finally:
        import gdal
