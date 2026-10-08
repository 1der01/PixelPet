# PixelPet - Project Information

## Running the Application

To run the PixelPet application:
```bash
python main.py
```

## Testing

Run all unit tests:
```bash
python -m unittest discover tests/ -v
```

Run specific test file:
```bash
python -m unittest tests.test_stats
python -m unittest tests.test_pet
```

Test coverage includes:
- `tests/test_stats.py` - Stat management (11 tests)
- `tests/test_mood.py` - Mood calculation (13 tests)
- `tests/test_progression.py` - Level and XP system (13 tests)
- `tests/test_pet.py` - Pet class and game logic (23 tests)
- `tests/test_events.py` - Random event system (13 tests)
- `tests/test_save_manager.py` - Save/load functionality (13 tests)

Total: 86 tests (all passing)

## Save Data Location

Save data is stored in the user's home directory:
- Windows: `C:\Users\<username>\.pixelpet\`
- Contains: `pet_save.json` and `settings.json`

## Project Structure

- `pixelpet/core/` - Game logic (pet, stats, mood, progression, events, activity monitoring, sound)
- `pixelpet/ui/` - UI components (pet window, interaction menu, setup window, settings window)
- `pixelpet/data/` - Data management (save manager, default data)
- `pixelpet/assets/` - Art and sound assets (pets, icons, sounds)
- `tests/` - Unit tests for core systems

## Key Features Implemented

- Pet creation with name, species, and random personality
- Four stats: Hunger, Energy, Happiness, Cleanliness
- Mood system based on stats
- Personality system with 7 different personalities
- Progression system with XP and level unlocks
- Random events with personality-specific dialogue
- Transparent floating pet window with idle animations (breathing, bouncing, blinking)
- Smart speech bubble positioning with fade animations
- Sound effects system (Windows beeps as fallback, supports WAV files)
- System tray integration
- Auto-save every minute
- Settings dialog with various options
- Pet reset functionality
- Comprehensive unit test coverage (86 tests)

## Dependencies

- PySide6 >= 6.6.0

## Development Notes

- The application uses PySide6 for Qt-based GUI
- Save data is stored in JSON format
- The pet window is frameless and transparent
- System tray provides show/hide and settings access
- Random events occur every 3 minutes with 30% probability
- Stats decay gradually over time (not punishing)
- Sound effects use Windows beeps as fallback if no sound files present
- To add actual sound files, place WAV files in `pixelpet/assets/sounds/`:
  - feed.wav, pet.wav, play.wav, clean.wav, sleep.wav
  - event.wav, level_up.wav, notification.wav
- All core game logic is tested with unit tests
- Tests use Python's built-in unittest framework
