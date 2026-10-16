import unittest
from unittest.mock import patch

from pixelpet.data.startup_manager import StartupManager


class FakeRegistryKey:
    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False


class FakeRegistry:
    HKEY_CURRENT_USER = object()
    KEY_SET_VALUE = 1
    REG_SZ = 2

    def __init__(self):
        self.values = {}

    def CreateKeyEx(self, *_args):
        return FakeRegistryKey()

    def OpenKey(self, *_args):
        return FakeRegistryKey()

    def SetValueEx(self, _key, name, _reserved, _kind, value):
        self.values[name] = value

    def DeleteValue(self, _key, name):
        if name not in self.values:
            raise FileNotFoundError(name)
        del self.values[name]


class StartupManagerTests(unittest.TestCase):
    def setUp(self):
        self.registry = FakeRegistry()

    def test_enable_registers_source_entry_point_for_current_user(self):
        with (
            patch("pixelpet.data.startup_manager.os.name", "nt"),
            patch.object(StartupManager, "_get_registry", return_value=self.registry),
        ):
            StartupManager.set_enabled(True)

        self.assertIn("PixelPet", self.registry.values)
        self.assertIn("main.py", self.registry.values["PixelPet"])

    def test_disable_removes_existing_startup_registration(self):
        self.registry.values["PixelPet"] = "old command"
        with (
            patch("pixelpet.data.startup_manager.os.name", "nt"),
            patch.object(StartupManager, "_get_registry", return_value=self.registry),
        ):
            StartupManager.set_enabled(False)

        self.assertNotIn("PixelPet", self.registry.values)

    def test_non_windows_registration_fails_explicitly(self):
        with patch("pixelpet.data.startup_manager.os.name", "posix"):
            with self.assertRaisesRegex(OSError, "only supported on Windows"):
                StartupManager.set_enabled(True)


if __name__ == "__main__":
    unittest.main()
