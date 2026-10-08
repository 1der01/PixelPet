"""Sound system for PixelPet."""
import os
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtCore import QUrl, QObject


class SoundSystem(QObject):
    """Manages sound effects for PixelPet."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.enabled = True
        self.sound_effects = {}
        self.load_sounds()

    def load_sounds(self):
        """Load sound effects from assets folder."""
        # Try to load sound files from assets
        assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "sounds")

        # Sound file mappings
        sound_files = {
            "feed": "feed.wav",
            "pet": "pet.wav",
            "play": "play.wav",
            "clean": "clean.wav",
            "sleep": "sleep.wav",
            "event": "event.wav",
            "level_up": "level_up.wav",
            "notification": "notification.wav",
        }

        for sound_name, filename in sound_files.items():
            file_path = os.path.join(assets_dir, filename)
            if os.path.exists(file_path):
                self.sound_effects[sound_name] = QUrl.fromLocalFile(file_path)
            else:
                # Use placeholder if file doesn't exist
                self.sound_effects[sound_name] = None

    def play(self, sound_name):
        """Play a sound effect."""
        if not self.enabled:
            return

        sound_url = self.sound_effects.get(sound_name)
        if sound_url:
            # Play actual sound file
            effect = QSoundEffect()
            effect.setSource(sound_url)
            effect.setVolume(0.5)
            effect.play()
        else:
            # Fall back to system beep if no sound file
            self.play_system_beep(sound_name)

    def play_system_beep(self, sound_name):
        """Play a system beep as fallback."""
        # Different beep patterns for different sounds
        import winsound
        import platform

        if platform.system() == "Windows":
            if sound_name == "feed":
                winsound.Beep(400, 100)
            elif sound_name == "pet":
                winsound.Beep(600, 100)
            elif sound_name == "play":
                winsound.Beep(800, 150)
            elif sound_name == "clean":
                winsound.Beep(500, 100)
            elif sound_name == "sleep":
                winsound.Beep(300, 200)
            elif sound_name == "event":
                winsound.Beep(700, 100)
            elif sound_name == "level_up":
                # Play ascending notes
                for freq in [400, 500, 600, 800]:
                    winsound.Beep(freq, 100)
            elif sound_name == "notification":
                winsound.Beep(1000, 200)
        else:
            # Fallback for non-Windows systems
            print("\a")  # System bell

    def set_enabled(self, enabled):
        """Enable or disable sound effects."""
        self.enabled = enabled

    def is_enabled(self):
        """Check if sound effects are enabled."""
        return self.enabled
