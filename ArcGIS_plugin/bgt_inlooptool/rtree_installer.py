import sys
from pathlib import Path

def ensure_rtree_install():
    current_dir = Path(__file__).parent
    custom_lib_dir = current_dir / "custom_libs"
    custom_lib_dir.mkdir(exist_ok=True)
    if not str(custom_lib_dir) in sys.path:
        sys.path.insert(0, str(custom_lib_dir))  # Note: prepend, not append!

    try:
        import rtree
        return
    except ImportError:
        from core import rtree_installer
        search_path = current_dir / "core" / "whls"
        wheel_filename = rtree_installer.get_wheel_filename(
            search_path=search_path,
            distribution="Rtree",
            python_tag_prefix="cp",
            abi_tag_suffix="m",
        )
        rtree_installer.unpack_whl(
            wheel_filename,
            package_name="rtree",
            extract_dir=custom_lib_dir
        )
    # Re-try import
    try:
        import rtree
        return
    except ImportError:
        raise