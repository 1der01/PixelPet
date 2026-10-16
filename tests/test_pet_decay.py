import unittest
from unittest.mock import patch

from pixelpet.core.pet import Pet


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


if __name__ == "__main__":
    unittest.main()
