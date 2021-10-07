from pathlib import Path
from zipfile import ZipFile
import platform
import sys
from typing import Union

def get_wheel_filename(search_path: Union[Path, str], distribution: str, version: str = None, python_tag_prefix = None,
                       abi_tag_suffix = ''):
    """ Find a wheel filename in search_path, using search criteria

    Warning: with regard to the platform tag, this function only makes a distinction between windows vs. linux vs. MacOS
    It does not distinguish between different platform versions or architectures (e.g. x86_64 vs. i686)

    Warning: this method does not work if the wheel includes a build tag

    The wheel filename is {distribution}-{version}(-{build tag})?-{python tag}-{abi tag}-{platform tag}.whl.
    See https://www.python.org/dev/peps/pep-0491/#id10

    :param search_path: directory where to look for wheels
    :param version: if not given, the first wheel that fits the other search criteria is returned
    :param distribution: python package to search wheels for
    :param python_tag_prefix: any of 'py' (generic python), 'cp' (CPython), 'ip' (IronPython), 'pp' (PyPy), jy (Jython).
    see https://www.python.org/dev/peps/pep-0425/#id11. if not given, python tag will be 'any'
    :param abi_tag_suffix: e.g. 'abi3', or 'm'. See https://www.python.org/dev/peps/pep-0425/#id12

    """
    python_major_version = sys.version_info[0]
    python_minor_version = sys.version_info[1]
    python_minor_version_proxy = python_minor_version
    while python_minor_version_proxy > 0: # proxy is used to find earlier version if current version is not available
        python_version_str = str(python_major_version) + str(python_minor_version_proxy)
        python_tag = python_tag_prefix + python_version_str
        abi_tag=python_tag + abi_tag_suffix

        platform_short_name = platform.platform(terse=True).lower()
        if 'win' in platform_short_name:
            platform_tag_platform = 'win'
        elif 'mac' in platform_short_name:
            platform_tag_platform = 'mac'
        else:
            platform_tag_platform = 'linux'

        pathlist = Path(search_path).rglob('*.whl')
        for path in pathlist:
            # because path is object not string
            wheel_stem = str(path.stem)
            keys = ['distribution', 'version', 'python_tag', 'abi_tag', 'platform_tag']
            wheel_dict = dict(zip(keys,wheel_stem.split('-')))
            print(wheel_dict)
            if wheel_dict['distribution'] == distribution and \
                    (version is None or wheel_dict['version'] == version) and \
                    (wheel_dict['python_tag'] == python_tag) and \
                    (wheel_dict['abi_tag'] == abi_tag) and \
                    (platform_tag_platform in wheel_dict['platform_tag']):
                return str(path)
        python_minor_version_proxy -= 1


def unpack_whl(whl_file, package_name, extract_dir):
    
    package_dir = extract_dir / package_name
    if not package_dir.is_dir():
        with ZipFile(whl_file, 'r') as zipObj:
           zipObj.extractall(extract_dir)

def unpack_rtree():
    
    plugin_path = Path(__file__).parent.parent
    search_path = Path(__file__).parent / 'whls'
    wheel_fn = get_wheel_filename(search_path=search_path, distribution='Rtree', python_tag_prefix='cp', abi_tag_suffix='m')
    
    unpack_whl(wheel_fn,
               package_name = 'rtree',
               extract_dir = plugin_path)
    