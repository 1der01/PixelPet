import unittest

from pixelpet.core.pet import Pet
from pixelpet.core.progression import Progression


class ProgressionCareGoalsTests(unittest.TestCase):
    def test_record_care_action_updates_affection_and_goal_progress(self):
        progression = Progression()

        progression.record_care_action("feed")
        progression.record_care_action("feed")

        self.assertEqual(progression.affection, 2)
        self.assertEqual(progression.goals["feed"]["progress"], 2)
        self.assertEqual(progression.get_goal_status()[0]["complete"], True)

    def test_pet_need_priority_ranks_critical_stats_for_ui_guidance(self):
        pet = Pet(name="Mochi", species="Cat")
        pet.stats.modify(hunger=-65, energy=-5, cleanliness=-20, happiness=-10)

        needs = pet.get_priority_needs()
        self.assertEqual(needs[0]["id"], "feed")
        self.assertEqual(needs[1]["id"], "clean")
        self.assertEqual(needs[2]["id"], "sleep")

    def test_level_unlocks_room_furniture(self):
        progression = Progression(level=1)
        self.assertEqual(progression.get_available_room_furniture(), ["Bed", "Plant"])

        progression.level = 2
        self.assertIn("Toy Box", progression.get_available_room_furniture())

        progression.level = 4
        self.assertEqual(
            progression.get_available_room_furniture(),
            ["Bed", "Plant", "Toy Box", "Lamp"],
        )

        self.assertEqual(
            progression.sanitize_room_furniture(["Lamp", "Plant", "Lamp", "Crown"]),
            ["Lamp", "Plant"],
        )

if __name__ == "__main__":
    unittest.main()
