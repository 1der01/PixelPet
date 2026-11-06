import json
import tempfile
import unittest
from datetime import datetime, timedelta

from pixelpet.core.pet import Pet
from pixelpet.data.save_manager import SaveManager


class SaveManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.save_manager = SaveManager(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_pet_creates_backup_before_overwriting(self):
        pet = Pet(name="Mochi", species="Cat")
        self.save_manager.save_pet(pet)

        pet.name = "Mochi v2"
        self.save_manager.save_pet(pet)

        backup_path = self.save_manager.save_file.parent / f"{self.save_manager.save_file.name}.bak"
        self.assertTrue(backup_path.exists())

        with open(backup_path, "r", encoding="utf-8") as backup_file:
            backup_data = json.load(backup_file)

        self.assertEqual(backup_data["name"], "Mochi")
        self.assertEqual(json.loads(self.save_manager.save_file.read_text(encoding="utf-8"))["name"], "Mochi v2")

    def test_backup_retention_keeps_recent_hourly_and_older_daily_snapshots(self):
        pet = Pet(name="Mochi", species="Cat")
        now = datetime.now().replace(minute=0, second=0, microsecond=0)
        snapshots = [
            now - timedelta(minutes=10),
            now - timedelta(minutes=30),
            now - timedelta(hours=3),
            now - timedelta(days=1, hours=1),
            now - timedelta(days=1, hours=2),
            now - timedelta(days=10),
            now - timedelta(days=31),
        ]
        for index, timestamp in enumerate(snapshots):
            backup_path = self.save_manager.backup_dir / (
                f"pet_save.json.{timestamp.strftime('%Y%m%d-%H%M%S_%f')}.bak"
            )
            backup_path.write_text(str(index), encoding="utf-8")

        self.save_manager._prune_backups(self.save_manager.save_file)

        backups = sorted(
            path.read_text(encoding="utf-8")
            for path in self.save_manager.backup_dir.glob("pet_save.json.*.bak")
        )
        self.assertEqual(backups, ["0", "2", "3", "5"])

    def test_corrupted_pet_save_recovers_and_restores_latest_valid_backup(self):
        pet = Pet(name="Mochi", species="Cat")
        self.save_manager.save_pet(pet)
        pet.name = "Updated Mochi"
        self.save_manager.save_pet(pet)
        self.save_manager.save_file.write_text("{broken", encoding="utf-8")

        recovered = self.save_manager.load_pet()

        self.assertEqual(recovered["name"], "Mochi")
        self.assertEqual(
            json.loads(self.save_manager.save_file.read_text(encoding="utf-8"))["name"],
            "Mochi",
        )

    def test_invalid_pet_save_without_valid_backup_returns_none(self):
        self.save_manager.save_file.write_text(
            json.dumps({"name": "Not a pet"}), encoding="utf-8"
        )

        self.assertIsNone(self.save_manager.load_pet())

    def test_export_and_import_save_round_trip(self):
        pet = Pet(name="Pip", species="Dog")
        self.save_manager.save_pet(pet)

        export_path = self.save_manager.save_dir / "exported_pet.json"
        exported = self.save_manager.export_save(export_path, save_type="pet")
        self.assertIsNotNone(exported)
        self.assertTrue(exported.exists())

        pet.name = "NewName"
        self.save_manager.save_pet(pet)

        imported = self.save_manager.import_save(export_path, save_type="pet")
        self.assertTrue(imported)
        self.assertEqual(json.loads(self.save_manager.save_file.read_text(encoding="utf-8"))["name"], "Pip")

    def test_import_rejects_invalid_pet_data_without_overwriting_current_save(self):
        pet = Pet(name="Mochi", species="Cat")
        self.save_manager.save_pet(pet)
        current_save = self.save_manager.save_file.read_text(encoding="utf-8")

        invalid_path = self.save_manager.save_dir / "invalid_pet.json"
        invalid_path.write_text(json.dumps({"name": "Not a pet"}), encoding="utf-8")

        self.assertFalse(self.save_manager.import_save(invalid_path))
        self.assertEqual(
            self.save_manager.save_file.read_text(encoding="utf-8"),
            current_save,
        )

    def test_import_rejects_malformed_nested_pet_data(self):
        invalid_path = self.save_manager.save_dir / "invalid_stats.json"
        invalid_path.write_text(
            json.dumps(
                {
                    "name": "Mochi",
                    "species": "Cat",
                    "stats": {"hunger": "full"},
                }
            ),
            encoding="utf-8",
        )

        self.assertFalse(self.save_manager.import_save(invalid_path))

    def test_import_rejects_non_finite_pet_stats(self):
        invalid_path = self.save_manager.save_dir / "non_finite_stats.json"
        invalid_path.write_text(
            '{"name":"Mochi","species":"Cat","stats":{"hunger":NaN}}',
            encoding="utf-8",
        )

        self.assertFalse(self.save_manager.import_save(invalid_path))

    def test_restore_pet_backup_restores_latest_save(self):
        pet = Pet(name="Mochi", species="Cat")
        self.save_manager.save_pet(pet)

        pet.name = "Mochi v2"
        self.save_manager.save_pet(pet)

        pet.name = "Mochi v3"
        self.save_manager.save_pet(pet)

        backup_path = self.save_manager.get_latest_backup(self.save_manager.save_file)
        self.assertIsNotNone(backup_path)
        self.assertTrue(self.save_manager.restore_pet_backup(backup_path))
        self.assertEqual(
            json.loads(self.save_manager.save_file.read_text(encoding="utf-8"))["name"],
            "Mochi v2",
        )

    def test_restore_pet_backup_rejects_invalid_backup(self):
        backup_path = self.save_manager.backup_dir / "invalid.bak"
        backup_path.write_text(json.dumps({"name": "Not a pet"}), encoding="utf-8")

        self.assertFalse(self.save_manager.restore_pet_backup(backup_path))


if __name__ == "__main__":
    unittest.main()
