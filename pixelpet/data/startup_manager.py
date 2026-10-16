"""Windows startup registration for PixelPet."""

import os
import subprocess
import sys
from pathlib import Path


class StartupManager:
    """Add or remove PixelPet from the current user's Windows startup apps."""

    RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
    VALUE_NAME = "PixelPet"

    @staticmethod
    def _get_registry():
        import winreg

        return winreg

    @classmethod
    def set_enabled(cls, enabled):
        """Register or unregister PixelPet for the current Windows user."""
        if os.name != "nt":
            raise OSError("Start with Windows is only supported on Windows.")

        registry = cls._get_registry()
        if enabled:
            if getattr(sys, "frozen", False):
                command = subprocess.list2cmdline([sys.executable])
            else:
                entry_point = Path(__file__).resolve().parents[2] / "main.py"
                command = subprocess.list2cmdline([sys.executable, str(entry_point)])
            with registry.CreateKeyEx(
                registry.HKEY_CURRENT_USER,
                cls.RUN_KEY,
                0,
                registry.KEY_SET_VALUE,
            ) as key:
                registry.SetValueEx(
                    key, cls.VALUE_NAME, 0, registry.REG_SZ, command
                )
            return

        try:
            with registry.OpenKey(
                registry.HKEY_CURRENT_USER,
                cls.RUN_KEY,
                0,
                registry.KEY_SET_VALUE,
            ) as key:
                registry.DeleteValue(key, cls.VALUE_NAME)
        except FileNotFoundError:
            pass
