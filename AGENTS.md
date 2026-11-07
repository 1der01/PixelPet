# PixelPet - Project Information

## Running the Application

To run the PixelPet application:
```bash
python main.py
```

## Testing

Run all unit tests:
```bash
python -m unittest discover -s tests -v
```

The suite currently covers activity service, app and settings behavior, pet
behavior and decay, the pet window, progression, save recovery, and Windows
startup registration. CI runs on Windows with Python 3.10, 3.12, and 3.14.

## Packaging

Install the project and runtime dependencies:
```bash
python -m pip install -e .
```

Build the portable Windows executable:
```powershell
python -m pip install -e ".[build]"
python -m PyInstaller --noconfirm --clean --onefile --windowed --name PixelPet main.py
```

## Save Data Location

Save data is stored in the user's home directory:
- Windows: `C:\Users\<username>\.pixelpet\`
- Contains: `pet_save.json` and `settings.json`

## Project Structure

- `pixelpet/core/` - Game logic (pet, stats, mood, progression, events, activity monitoring, sound)
- `pixelpet/ui/` - UI components (pet window, interaction menu, setup window, settings window)
- `pixelpet/data/` - Data management (save manager, default data)
- `tests/` - Unit tests for game logic, UI, persistence, and settings
- `pyproject.toml` - Project metadata, dependencies, and build extra

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
- Unit tests for core logic, persistence, UI behavior, and settings

## Dependencies

- Python >= 3.10
- PySide6 >= 6.6.0
- PyInstaller >= 6.11 (optional; for Windows executable builds)

## Development Notes

- The application uses PySide6 for Qt-based GUI
- Save data is stored in JSON format
- The pet window is frameless and transparent
- System tray provides show/hide and settings access
- Random events occur every 3 minutes with 30% probability
- Stats decay gradually over time (not punishing)
- Sound effects use Windows beeps as fallback if no sound files present
- Optional sound files can be placed in `pixelpet/assets/sounds/`:
  - feed.wav, pet.wav, play.wav, clean.wav, sleep.wav
  - event.wav, level_up.wav, notification.wav
- All core game logic is tested with unit tests
- Tests use Python's built-in unittest framework
