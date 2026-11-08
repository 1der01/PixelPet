# Contributing to PixelPet

Thanks for helping improve PixelPet! Bug reports, feature ideas, documentation
updates, and pull requests are welcome.

## Set up a development environment

Use Python 3.10 or newer. From the repository root, create and activate a
virtual environment in PowerShell, then install the project:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

To build the portable Windows executable, install the optional build
dependency:

```powershell
python -m pip install -e ".[build]"
python -m PyInstaller --noconfirm --clean --onefile --windowed --name PixelPet main.py
```

## Before opening a pull request

- Run the unit tests: `python -m unittest discover -s tests -v`
- Keep changes focused and add or update tests for behavior changes.
- Update the README when user-facing behavior or setup instructions change.
- Check that your change does not include save files, credentials, or other
  personal data.
- Describe the problem, the solution, and how you verified it in the pull
  request.

The GitHub Actions workflow runs tests on Windows with Python 3.10, 3.12, and
3.14 and builds the portable executable.

## Reporting issues

Use the issue templates for bug reports and feature requests. For bugs, include
the steps to reproduce and what you expected versus what happened. Do not
attach your `.pixelpet` save files; they can contain personal pet data.
