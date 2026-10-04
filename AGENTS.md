# PixelPet - Project Information

## Running the Application

To run the PixelPet application:
```bash
python main.py
```

## Testing

Core logic tests can be run by importing and testing individual modules:
- `pixelpet.core.pet` - Pet class and game logic
- `pixelpet.core.stats` - Stat management
- `pixelpet.core.mood` - Mood calculation
- `pixelpet.core.progression` - Level and XP system
- `pixelpet.data.save_manager` - Save/load functionality

## Save Data Location

Save data is stored in the user's home directory:
- Windows: `C:\Users\<username>\.pixelpet\`
- Contains: `pet_save.json` and `settings.json`

## Project Structure

- `pixelpet/core/` - Game logic (pet, stats, mood, progression, events, activity monitoring)
- `pixelpet/ui/` - UI components (pet window, interaction menu, setup window, settings window)
- `pixelpet/data/` - Data management (save manager, default data)
- `pixelpet/assets/` - Art and sound assets (pets, icons, sounds)

## Key Features Implemented

- Pet creation with name, species, and random personality
- Four stats: Hunger, Energy, Happiness, Cleanliness
- Mood system based on stats
- Personality system with 7 different personalities
- Progression system with XP and level unlocks
- Random events with personality-specific dialogue
- Transparent floating pet window
- System tray integration
- Auto-save every minute
- Settings dialog with various options
- Pet reset functionality

## Dependencies

- PySide6 >= 6.6.0

## Development Notes

- The application uses PySide6 for Qt-based GUI
- Save data is stored in JSON format
- The pet window is frameless and transparent
- System tray provides show/hide and settings access
- Random events occur every 3 minutes with 30% probability
- Stats decay gradually over time (not punishing)
