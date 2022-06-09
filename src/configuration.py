import ctypes
import os
import platform


def setup_hidden_dir():
    """Setups the configuration for hidden directory"""
    dir_path = os.path.expanduser(r"~\.ONKO_HIDDEN_DICOM")
    os.environ['DICOM_HIDDEN_DIR'] = dir_path

    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        if platform.system() == 'Windows':
            ctypes.windll.kernel32.SetFileAttributesW(dir_path,
                                                      0x02)
