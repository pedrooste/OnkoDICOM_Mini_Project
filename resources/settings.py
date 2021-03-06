"""
Loads the application settings from DB
"""
import logging
import os

from resources.settings_connection import SettingsConnection

LOG_FILES_DIR = 'logs'
if not os.path.isdir(LOG_FILES_DIR):
    os.makedirs(LOG_FILES_DIR)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('logs/settings.log', mode='w')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def load_settings(user_id):
    """loads settings stored in the DB"""
    database = SettingsConnection()

    try:
        db_result = database.get_setting(user_id)
        if db_result is False:
            raise AttributeError("Could not return settings, setting default")
        return Settings(*db_result)
    except (AttributeError, TypeError) as err:
        logging.warning(err)
        return Settings()


class Settings:
    """Stores settings used throughout the program"""

    def __init__(self, user_id=1, window_x=500, window_y=500, force_open=False, dicom_path=''):
        self.user_id = user_id
        self.window_x = window_x
        self.window_y = window_y
        self.force_open = force_open
        self.dicom_path = dicom_path

        self.log_settings()

    def log_settings(self):
        """logs settings object for debugging"""
        logger.info(
            "id: %s, window: %sx %sy, force open: %s, DICOM path: %s",
            self.user_id, self.window_x, self.window_y, self.force_open, self.dicom_path
        )
