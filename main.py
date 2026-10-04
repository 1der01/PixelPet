"""Main entry point for PixelPet application."""
import sys
import os

# Add the pixelpet directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pixelpet.main import main

if __name__ == "__main__":
    main()
