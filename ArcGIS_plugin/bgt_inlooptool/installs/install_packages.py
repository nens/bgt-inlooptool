# https://stackoverflow.com/questions/12332975/installing-python-module-within-code
import subprocess
import sys
import os


def try_install_gdal():


    # python_version = str(sys.version)[0]
    try:
        print("Trying to import gdal")
        import gdal
    except ImportError:
        print("gdal is not installed, trying to install gdal")
        # TODO check pip version if this has to be run
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        current_folder = os.path.dirname(__file__)
        wheel = os.path.join(current_folder, 'GDAL-2.2.4-cp27-cp27m-win32.whl')
        subprocess.check_call([sys.executable, "-m", "pip", "install", wheel])
        print("gdal is succesfully installed")
    finally:
        import gdal
        print("gdal is succesfully imported")
        # if python_version == '2':
        #     raw_input("Press enter to exit")
        # elif python_version == '3':
        #     input("Press enter to exit")


if __name__ == '__main__':
    try_install_gdal()


