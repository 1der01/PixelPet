import unittest
import tempfile
from unittest.mock import Mock, patch

from pixelpet.core.pet import Pet
from pixelpet.data.save_manager import SaveManager


class PetStatDecayTests(unittest.TestCase):
    def test_stats_do_not_decay_before_one_interval(self):
        pet = Pet()
        initial_stats = pet.stats.to_dict()

        with patch("pixelpet.core.events.random.random", return_value=1.0):
            pet.update(pet.STAT_DECAY_INTERVAL - 1)

        self.assertEqual(pet.stats.to_dict(), initial_stats)

    def test_stats_decay_once_at_interval_boundary(self):
        pet = Pet()

        with patch("pixelpet.core.events.random.random", return_value=1.0):
            pet.update(pet.STAT_DECAY_INTERVAL)

        self.assertEqual(pet.stats.hunger, 68)
        self.assertEqual(pet.stats.energy, 49)
        self.assertEqual(pet.stats.happiness, 79)
        self.assertEqual(pet.stats.cleanliness, 59)

    def test_large_update_applies_all_elapsed_decay_periods(self):
        pet = Pet()

        with patch("pixelpet.core.events.random.random", return_value=1.0):
            pet.update(pet.STAT_DECAY_INTERVAL * 3)

        self.assertEqual(pet.stats.hunger, 64)
        self.assertEqual(pet.stats.energy, 47)
        self.assertEqual(pet.stats.happiness, 77)
        self.assertEqual(pet.stats.cleanliness, 57)

    def test_sleeping_pet_does_not_accumulate_stat_decay(self):
        pet = Pet()
        pet.is_sleeping = True
        initial_stats = pet.stats.to_dict()

        with patch("pixelpet.core.events.random.random", return_value=1.0):
            pet.update(pet.STAT_DECAY_INTERVAL * 2)
            pet.is_sleeping = False
            pet.update(pet.STAT_DECAY_INTERVAL - 1)

        self.assertEqual(pet.stats.to_dict(), initial_stats)

    def test_waking_after_a_long_pause_does_not_decay_while_previously_asleep(self):
        pet = Pet()
        pet.is_sleeping = True
        pet.activity_monitor.update = Mock(return_value=True)
        initial_stats = pet.stats.to_dict()

        with patch("pixelpet.core.events.random.random", return_value=1.0):
            pet.update(pet.STAT_DECAY_INTERVAL * 2)

        self.assertFalse(pet.is_sleeping)
        self.assertEqual(
            pet.stats.to_dict(),
            {**initial_stats, "energy": min(100, initial_stats["energy"] + 30)},
        )

    def test_stats_remain_unchanged_after_loading_an_old_save(self):
        with tempfile.TemporaryDirectory() as save_dir:
            save_manager = SaveManager(save_dir)
            pet = Pet()
            initial_stats = pet.stats.to_dict()
            save_manager.save_pet(pet)

            loaded_pet = Pet.from_dict(save_manager.load_pet())
            loaded_pet.update(1)

            self.assertEqual(loaded_pet.stats.to_dict(), initial_stats)


if __name__ == "__main__":
    unittest.main()
