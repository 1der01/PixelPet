import unittest
from types import SimpleNamespace

from pixelpet.data.activity_service import ActivityService


class FakeInsertQuery:
    def __init__(self, response):
        self.response = response

    def execute(self):
        return self.response


class FakeActivityTable:
    def __init__(self, response):
        self.response = response
        self.inserted_values = None

    def insert(self, values):
        self.inserted_values = values
        return FakeInsertQuery(self.response)


class FakeAuthClient:
    def __init__(self, user):
        self.user = user

    def get_user(self):
        return SimpleNamespace(user=self.user)


class FakeSupabaseClient:
    def __init__(self, user, response):
        self.auth = FakeAuthClient(user)
        self.activity_table = FakeActivityTable(response)
        self.requested_table = None

    def table(self, table_name):
        self.requested_table = table_name
        return self.activity_table


class ActivityServiceTests(unittest.TestCase):
    def setUp(self):
        self.inserted_activity = {
            "id": "activity-1",
            "user_id": "user-1",
            "title": "Feed the pet",
            "description": "Give Mochi a snack",
            "status": "pending",
        }
        self.client = FakeSupabaseClient(
            SimpleNamespace(id="user-1"),
            SimpleNamespace(data=[self.inserted_activity]),
        )
        self.service = ActivityService(self.client)

    def test_create_activity_inserts_validated_fields_for_authenticated_user(self):
        result = self.service.create_activity(
            title="  Feed the pet ",
            description=" Give Mochi a snack ",
            status="in_progress",
        )

        self.assertIs(result, self.inserted_activity)
        self.assertEqual(self.client.requested_table, "activities")
        self.assertEqual(
            self.client.activity_table.inserted_values,
            {
                "user_id": "user-1",
                "title": "Feed the pet",
                "description": "Give Mochi a snack",
                "status": "in_progress",
            },
        )

    def test_create_activity_rejects_empty_title_before_supabase_calls(self):
        with self.assertRaisesRegex(ValueError, "title cannot be empty"):
            self.service.create_activity(title="  ")

        self.assertIsNone(self.client.requested_table)

    def test_create_activity_rejects_invalid_status_before_supabase_calls(self):
        with self.assertRaisesRegex(ValueError, "Activity status"):
            self.service.create_activity(title="Feed the pet", status="archived")

        self.assertIsNone(self.client.requested_table)

    def test_create_activity_requires_authenticated_user(self):
        client = FakeSupabaseClient(
            None, SimpleNamespace(data=[self.inserted_activity])
        )
        service = ActivityService(client)

        with self.assertRaisesRegex(RuntimeError, "authenticated Supabase user"):
            service.create_activity(title="Feed the pet")

        self.assertIsNone(client.requested_table)

    def test_create_activity_reports_missing_inserted_row(self):
        client = FakeSupabaseClient(
            SimpleNamespace(id="user-1"), SimpleNamespace(data=[])
        )
        service = ActivityService(client)

        with self.assertRaisesRegex(RuntimeError, "did not return"):
            service.create_activity(title="Feed the pet")


if __name__ == "__main__":
    unittest.main()
