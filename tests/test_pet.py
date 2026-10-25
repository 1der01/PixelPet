import unittest

from pixelpet.core.pet import Pet


class PetSerializationTests(unittest.TestCase):
    def test_from_dict_restores_sleep_state_and_created_time(self):
        pet_data = {
            "name": "Mochi",
            "species": "Cat",
            "personality": "Lazy",
            "favorite_food": "Fish",
            "stats": {
                "hunger": 34,
                "energy": 12,
                "happiness": 76,
                "cleanliness": 52,
            },
            "progression": {
                "level": 3,
                "experience": 140,
                "inventory": ["Hat"],
                "achievements": ["First friend"],
            },
            "age": 8.5,
            "mood": "Sleepy",
            "is_sleeping": True,
            "created_time": 987654321,
            "room_theme": "Space",
            "room_furniture": ["Lamp"],
        }

        pet = Pet.from_dict(pet_data)

        self.assertEqual(pet.name, "Mochi")
        self.assertEqual(pet.species, "Cat")
        self.assertTrue(pet.is_sleeping)
        self.assertEqual(pet.created_time, 987654321)
        self.assertEqual(pet.age, 8.5)
        self.assertEqual(pet.room_theme, "Space")
        self.assertEqual(pet.room_furniture, ["Lamp"])

    def test_to_dict_includes_room_data(self):
        pet = Pet(name="Pip", species="Dog", room_theme="Garden", room_furniture=["Toy Box"])

        data = pet.to_dict()

        self.assertEqual(data["room_theme"], "Garden")
        self.assertEqual(data["room_furniture"], ["Toy Box"])

    def test_pet_name_and_species_are_normalized(self):
        pet = Pet(name="  Luna 2!!!  ", species="cat")

        self.assertEqual(pet.name, "Luna 2")
        self.assertEqual(pet.species, "Cat")
        self.assertEqual(pet.favorite_food, "Fish")

    def test_invalid_names_fall_back_to_default(self):
        pet = Pet(name="!!!@@@", species="Alien")

        self.assertEqual(pet.name, "Mochi")
        self.assertIn(pet.species, Pet.SPECIES)


if __name__ == "__main__":
    unittest.main()
