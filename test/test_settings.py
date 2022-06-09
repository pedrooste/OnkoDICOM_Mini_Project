"""This document is to test loading the settings"""
from resources.settings import Settings, load_settings
from resources.settings_connection import SettingsConnection


def test_clearing_table():
    """Clearing existing tables ready for testing"""
    conn = SettingsConnection()
    conn.connection.cursor().execute("DROP TABLE IF EXISTS SETTINGS")


def test_setup():
    """ Testing Db setup"""
    conn = SettingsConnection()
    setting = Settings(1, 500, 600, True, 'path')
    assert conn.insert_or_update_setting(setting) == 1


def test_load_settings():
    """Testing that settings can be loaded from the DB"""
    assert load_settings(1).log_settings() == Settings(1, 500, 600, True, 'path').log_settings()


def test_load_default_settings():
    """When loading settings that dont exist, the default settings will be returned"""
    assert load_settings(4).log_settings() == Settings(1, 400, 500, False, '').log_settings()
