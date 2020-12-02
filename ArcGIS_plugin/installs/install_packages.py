
import sys
import os

# https://stackoverflow.com/questions/12332975/installing-python-module-within-code
import subprocess
from subprocess import CalledProcessError

# https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal
WHEEL = os.path.join(os.path.dirname(__file__), 'GDAL-2.2.4-cp27-cp27m-win32.whl')
python_version = int(str(sys.version)[0])

def try_install_gdal():
    """
    This script tries to import gdal, else install it without and with a pip upgrade

    If run from bgt_inlooptool_ArcGIS.py then I get an error: 'could not find file: pip.mxd' and Arcmap wont start
    Running from the toolbox .pyt just gives an import osr error and does not work to install it.
    The script has to be run manually
    """

    try:
        import gdal
        print("gdal is succesvol geimporteerd")
    except ImportError as ex:
        if python_version == 2:
            try:
                print("gdal kon niet geimporteerd worden, nu wordt geprobeerd om gdal te installeren")
                subprocess.check_call([sys.executable, "-m", "pip", "install", WHEEL])
                import gdal
                print("gdal is succesvol geinstalleerd")
            except CalledProcessError as ex2:  # uitzoeken wat voor error
                try:
                    print("gdal kan niet direct geinstalleerd worden, nu wordt geprobeerd pip te upgraden")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
                    subprocess.check_call([sys.executable, "-m", "pip", "install", WHEEL])
                    import gdal
                    print("gdal is succesvol geinstalleerd")
                except CalledProcessError as ex3:
                    print("pip is niet geupdate en gdal kon niet worden geinstalleerd.")
                    print("Neem contact op met bgtinlooptool@nelen-schuurmans.nl")
        else:
            print("gdal zou geinstalleerd moeten zijn in ArcGIS Pro. Check in ArcGIS Pro of gdal geinstalleerd is")
            print(" of neem contact op met uw IT afdeling of desnoods met Esri")


if __name__ == '__main__':
    try_install_gdal()


