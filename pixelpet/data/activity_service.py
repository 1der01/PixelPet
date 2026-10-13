"""Service layer for creating and validating pet activities."""

from __future__ import annotations


class ActivityService:
    """Manage activity records in the Supabase-backed activity table."""

    VALID_STATUSES = {"pending", "in_progress", "completed", "cancelled"}

    def __init__(self, client):
        self.client = client

    @staticmethod
    def _normalize_text(value):
        if value is None:
            return ""
        return str(value).strip()

    def _get_authenticated_user(self):
        if self.client is None:
            return None

        auth = getattr(self.client, "auth", None)
        if auth is None:
            return None

        try:
            user_response = auth.get_user()
        except AttributeError:
            return None

        if user_response is None:
            return None

        if hasattr(user_response, "user"):
            return user_response.user
        if isinstance(user_response, dict):
            return user_response.get("user")
        return user_response

    def create_activity(self, title, description="", status="pending"):
        """Create an activity record for the authenticated user."""
        cleaned_title = self._normalize_text(title)
        if not cleaned_title:
            raise ValueError("title cannot be empty")

        cleaned_status = self._normalize_text(status)
        if cleaned_status not in self.VALID_STATUSES:
            valid = ", ".join(sorted(self.VALID_STATUSES))
            raise ValueError(f"Activity status '{status}' is invalid. Allowed values: {valid}")

        user = self._get_authenticated_user()
        if user is None:
            raise RuntimeError("No authenticated Supabase user available")

        user_id = getattr(user, "id", None)
        if user_id is None and isinstance(user, dict):
            user_id = user.get("id")
        if user_id is None:
            raise RuntimeError("No authenticated Supabase user available")

        payload = {
            "user_id": user_id,
            "title": cleaned_title,
            "description": self._normalize_text(description),
            "status": cleaned_status,
        }

        table = self.client.table("activities")
        response = table.insert(payload).execute()

        if response is None or not getattr(response, "data", None):
            raise RuntimeError("Insert did not return a row for the new activity")

        return response.data[0]
