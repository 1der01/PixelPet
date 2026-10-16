"""Save manager for PixelPet - handles JSON persistence."""
import json
import logging
import math
import os
import shutil
import tempfile
import time
from datetime import datetime
from pathlib import Path


logger = logging.getLogger(__name__)


class SaveManager:
    """Manages saving and loading pet data."""

    MAX_BACKUPS = 20

    def __init__(self, save_dir=None):
        if save_dir is None:
            # Use user's home directory for saves
            self.save_dir = Path.home() / ".pixelpet"
        else:
            self.save_dir = Path(save_dir)

        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir = self.save_dir / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.save_file = self.save_dir / "pet_save.json"
        self.settings_file = self.save_dir / "settings.json"

    def _backup_file(self, file_path):
        """Create a backup copy before overwriting a JSON save file."""
        if file_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S_%f")
            backup_path = self.backup_dir / f"{file_path.name}.{timestamp}.bak"
            shutil.copy2(file_path, backup_path)

            # Keep a quick-access latest backup for simple restore flows.
            latest_backup = file_path.with_name(f"{file_path.name}.bak")
            shutil.copy2(file_path, latest_backup)
            self._prune_backups(file_path)
            return backup_path
        return None

    def _prune_backups(self, file_path):
        """Keep only the most recent timestamped backups for a save file."""
        backups = sorted(
            self.backup_dir.glob(f"{file_path.name}.*.bak"),
            key=lambda path: path.name,
            reverse=True,
        )
        for backup_path in backups[self.MAX_BACKUPS:]:
            backup_path.unlink()

    def backup_file(self, file_path):
        """Create a timestamped backup for a save file and return its path."""
        if not file_path.exists():
            return None

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S_%f")
        backup_path = self.backup_dir / f"{file_path.name}.{timestamp}.bak"
        shutil.copy2(file_path, backup_path)

        latest_backup = file_path.with_name(f"{file_path.name}.bak")
        shutil.copy2(file_path, latest_backup)
        self._prune_backups(file_path)
        return backup_path

    def restore_backup(self, file_path, backup_path=None):
        """Restore a save file from its latest backup or an explicit backup path."""
        if backup_path is None:
            backup_path = self.get_latest_backup(file_path)

        backup_path = Path(backup_path)
        if not backup_path.exists():
            return False

        shutil.copy2(backup_path, file_path)
        return True

    def get_latest_backup(self, file_path):
        """Return the newest backup for the given save file."""
        pattern = f"{file_path.name}.*.bak"
        backup_candidates = sorted(self.backup_dir.glob(pattern), key=lambda path: path.stat().st_mtime, reverse=True)
        if backup_candidates:
            return backup_candidates[0]

        latest_backup = file_path.with_name(f"{file_path.name}.bak")
        if latest_backup.exists():
            return latest_backup
        return None

    def backup_pet_save(self):
        """Create a manual backup of the current pet save."""
        return self.backup_file(self.save_file)

    def restore_pet_backup(self, backup_path=None):
        """Restore the pet save from the latest backup."""
        if backup_path is None:
            backup_path = self.get_latest_backup(self.save_file)
        if backup_path is None or not self._is_valid_pet_save_file(backup_path):
            return False
        return self.restore_backup(self.save_file, backup_path)

    @staticmethod
    def _is_valid_pet_save(data):
        """Check that imported pet data has the structure understood by PixelPet."""
        if not isinstance(data, dict):
            return False

        if not isinstance(data.get("name"), str) or not data["name"].strip():
            return False
        if data.get("species") not in ("Cat", "Dog", "Blob", "Frog", "Robot"):
            return False

        def is_number(value):
            if isinstance(value, bool):
                return False
            if isinstance(value, int):
                return True
            return isinstance(value, float) and math.isfinite(value)

        for key in ("age", "created_time", "last_saved"):
            if key in data and not is_number(data[key]):
                return False
        for key in ("personality", "mood", "room_theme"):
            if key in data and not isinstance(data[key], str):
                return False
        if "is_sleeping" in data and not isinstance(data["is_sleeping"], bool):
            return False

        furniture = data.get("room_furniture")
        if furniture is not None and (
            not isinstance(furniture, list)
            or not all(isinstance(item, str) for item in furniture)
        ):
            return False

        stats = data.get("stats", {})
        if not isinstance(stats, dict) or any(
            not is_number(value) for value in stats.values()
        ):
            return False

        progression = data.get("progression", {})
        if not isinstance(progression, dict):
            return False
        for key in ("level", "experience", "affection", "care_streak"):
            if key in progression and not is_number(progression[key]):
                return False
        for key in ("inventory", "achievements"):
            if key in progression and (
                not isinstance(progression[key], list)
                or not all(isinstance(item, str) for item in progression[key])
            ):
                return False
        equipped = progression.get("equipped_accessory")
        if equipped is not None and not isinstance(equipped, str):
            return False
        goals = progression.get("goals")
        if goals is not None:
            if not isinstance(goals, dict):
                return False
            for goal in goals.values():
                if (
                    not isinstance(goal, dict)
                    or not isinstance(goal.get("title"), str)
                    or not is_number(goal.get("target"))
                    or not is_number(goal.get("progress"))
                ):
                    return False

        return True

    @classmethod
    def _is_valid_pet_save_file(cls, file_path):
        """Read and validate a pet save without modifying it."""
        try:
            with open(file_path, "r", encoding="utf-8") as save_file:
                return cls._is_valid_pet_save(json.load(save_file))
        except (OSError, ValueError):
            return False

    def export_save(self, file_path, save_type="pet"):
        """Export a save file to another location without altering the current save."""
        source = self.save_file if save_type == "pet" else self.settings_file
        if not source.exists():
            return None

        destination = Path(file_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        return destination

    def import_save(self, file_path, save_type="pet"):
        """Import a save file from another location, creating a backup beforehand."""
        source = Path(file_path)
        if not source.exists():
            return False

        target = self.save_file if save_type == "pet" else self.settings_file
        try:
            with open(source, "r", encoding="utf-8") as imported_file:
                imported_data = json.load(imported_file)
        except (OSError, ValueError):
            return False

        if save_type == "pet" and not self._is_valid_pet_save(imported_data):
            return False

        self._backup_file(target)
        shutil.copy2(source, target)
        return True

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
        except Exception:
            logger.exception("Error saving %s", file_path.name)
            if temp_path and temp_path.exists():
                temp_path.unlink(missing_ok=True)
            return False

    def save_pet(self, pet):
        """Save pet data to JSON file."""
        try:
            data = pet.to_dict()
            data["last_saved"] = int(time.time())
            return self._atomic_write_json(self.save_file, data)
        except Exception:
            logger.exception("Error saving pet")
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
            logger.error("Corrupted save file, will create new pet")
            return None
        except Exception:
            logger.exception("Error loading pet")
            return None

    def save_settings(self, settings):
        """Save settings to JSON file."""
        try:
            return self._atomic_write_json(self.settings_file, settings)
        except Exception:
            logger.exception("Error saving settings")
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
            logger.error(
                "Corrupted settings file, will use defaults"
            )
            return None
        except Exception:
            logger.exception("Error loading settings")
            return None

    def delete_save(self):
        """Delete save file."""
        try:
            if self.save_file.exists():
                self.save_file.unlink()
            return True
        except Exception:
            logger.exception("Error deleting save")
            return False

    def has_save(self):
        """Check if save file exists."""
        return self.save_file.exists()
