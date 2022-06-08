import ctypes
import os
import platform
import logging
LOG_FILES_DIR = '../logs'
if not os.path.isdir(LOG_FILES_DIR):
    os.makedirs(LOG_FILES_DIR)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('../logs/onko_dicom.log', mode='w')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def setup_configuration():
    """Setups the configuration for hidden directory"""
    logger.info("Configuring the hidden directory")
    dir_path = os.path.expanduser("~\.ONKO_HIDDEN_DICOM")
    os.environ['DICOM_HIDDEN_DIR'] = dir_path

    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        if platform.system() == 'Windows':
            ctypes.windll.kernel32.SetFileAttributesW(dir_path,
                                                      0x02)
    logger.info("Configuration Complete")