"""Save manager for PixelPet - handles JSON persistence."""
import json
import os
import shutil
import tempfile
import time
from pathlib import Path


class SaveManager:
    """Manages saving and loading pet data."""

    def __init__(self, save_dir=None):
        if save_dir is None:
            # Use user's home directory for saves
            self.save_dir = Path.home() / ".pixelpet"
        else:
            self.save_dir = Path(save_dir)

        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.save_file = self.save_dir / "pet_save.json"
        self.settings_file = self.save_dir / "settings.json"

    def _backup_file(self, file_path):
        """Create a backup copy before overwriting a JSON save file."""
        if file_path.exists():
            backup_path = file_path.with_name(f"{file_path.name}.bak")
            shutil.copy2(file_path, backup_path)
        return file_path.with_name(f"{file_path.name}.bak")

    def _atomic_write_json(self, file_path, payload):
        """Write JSON payload safely so data is not lost on a crash or interruption."""
        self._backup_file(file_path)

        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(
                "w",
                dir=str(file_path.parent),
                prefix=f"{file_path.name}.",
                suffix=".tmp",
                delete=False,
                encoding="utf-8",
            ) as temp_file:
                json.dump(payload, temp_file, indent=2)
                temp_path = Path(temp_file.name)

            os.replace(temp_path, file_path)
            return True
        except Exception as exc:
            print(f"Error saving {file_path.name}: {exc}")
            if temp_path and temp_path.exists():
                temp_path.unlink(missing_ok=True)
            return False

    def save_pet(self, pet):
        """Save pet data to JSON file."""
        try:
            data = pet.to_dict()
            data["last_saved"] = int(time.time())
            return self._atomic_write_json(self.save_file, data)
        except Exception as e:
            print(f"Error saving pet: {e}")
            return False

    def load_pet(self):
        """Load pet data from JSON file."""
        try:
            if not self.save_file.exists():
                return None

            with open(self.save_file, "r") as f:
                data = json.load(f)

            return data
        except json.JSONDecodeError:
            print("Corrupted save file, will create new pet")
            return None
        except Exception as e:
            print(f"Error loading pet: {e}")
            return None

    def save_settings(self, settings):
        """Save settings to JSON file."""
        try:
            return self._atomic_write_json(self.settings_file, settings)
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False

    def load_settings(self):
        """Load settings from JSON file."""
        try:
            if not self.settings_file.exists():
                return None

            with open(self.settings_file, "r") as f:
                data = json.load(f)

            return data
        except json.JSONDecodeError:
            print("Corrupted settings file, will use defaults")
            return None
        except Exception as e:
            print(f"Error loading settings: {e}")
            return None

    def delete_save(self):
        """Delete save file."""
        try:
            if self.save_file.exists():
                self.save_file.unlink()
            return True
        except Exception as e:
            print(f"Error deleting save: {e}")
            return False

    def has_save(self):
        """Check if save file exists."""
        return self.save_file.exists()
