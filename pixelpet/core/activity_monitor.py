"""Activity monitor for PixelPet - detects user computer activity."""
import time


class ActivityMonitor:
    """Lightweight user activity detection."""

    def __init__(self):
        self.last_activity_time = time.time()
        self.idle_threshold = 300  # 5 minutes of inactivity
        self.is_idle = False

    def update(self):
        """Update activity status."""
        current_time = time.time()
        time_since_activity = current_time - self.last_activity_time

        was_idle = self.is_idle
        self.is_idle = time_since_activity > self.idle_threshold

        # Return True if user just became active after being idle
        return was_idle and not self.is_idle

    def record_activity(self):
        """Record user activity."""
        self.last_activity_time = time.time()

    def is_user_idle(self):
        """Check if user is currently idle."""
        return self.is_idle

    def get_idle_duration(self):
        """Get how long user has been idle in seconds."""
        if not self.is_idle:
            return 0
        return time.time() - self.last_activity_time
