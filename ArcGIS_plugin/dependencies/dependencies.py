#! C:/Users/hsc/AppData/Local/ESRI/conda/envs/arcgispro-py3-clone/python

import sys
import os

# https://stackoverflow.com/questions/12332975/installing-python-module-within-code
import subprocess
from subprocess import CalledProcessError


def install_rtree():
    """
    This script tries to import rtree, else install it without and with a pip upgrade

    If run from bgt_inlooptool_ArcGIS.py then I get an error: 'could not find file: pip.mxd' and Arcmap wont start
    Running from the toolbox .pyt just gives an import osr error and does not work to install it.
    The script has to be run manually
    """

    try:
        import rtree
        print("rtree is succesvol geimporteerd")
        input("Press enter to exit")
    except ImportError as ex:
        try:
            print("rtree kon niet geimporteerd worden, nu wordt geprobeerd om rtree te installeren")
            subprocess.check_call([sys.executable, "-m", "pip", "install", 'rtree'])
            import rtree
            print("rtree is succesvol geinstalleerd")
        except CalledProcessError as ex2:  # uitzoeken wat voor error
            try:
                print("rtree kan niet direct geinstalleerd worden, nu wordt geprobeerd pip te upgraden")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade"])
                subprocess.check_call([sys.executable, "-m", "pip", "install", 'rtree'])
                import rtree
                print("rtree is succesvol geinstalleerd")
            except CalledProcessError as ex3:
                print("pip is niet geupdate en rtree kon niet worden geinstalleerd.")
                print("Neem contact op met bgtinlooptool@nelen-schuurmans.nl")
        input("Press enter to exit")


if __name__ == '__main__':
    install_rtree()


