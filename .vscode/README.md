# VS Code Configuration

This directory contains VS Code workspace settings for the he6o-api project.

## Extensions Required

Install the recommended extensions when prompted, or manually install:

- **Python** (`ms-python.python`) - Python language support
- **Pylance** (`ms-python.vscode-pylance`) - Fast Python language server
- **Ruff** (`charliermarsh.ruff`) - Fast Python linter and formatter
- **Black Formatter** (`ms-python.black-formatter`) - Python code formatter
- **isort** (`ms-python.isort`) - Import statement organizer
- **mypy Type Checker** (`ms-python.mypy-type-checker`) - Static type checker
- **flake8** (`ms-python.flake8`) - Python style guide checker

## Features

### Automatic Formatting

- **Format on Save**: Enabled for Python files
- **Default Formatter**: Ruff (fast and modern)
- **Import Organization**: Automatically organizes imports on save

### Code Quality Tools

All tools are configured to use settings from `.code_quality/`:

- **Ruff**: Linting and formatting (`.code_quality/ruff.toml`)
- **Black**: Code formatting (`.code_quality/black.toml`)
- **isort**: Import sorting (`.code_quality/isort.cfg`)
- **mypy**: Type checking (`.code_quality/mypy.ini`)
- **flake8**: Style checking (`.code_quality/.flake8`)

### Editor Settings

- **Line Length**: 79 characters (PEP 8 compliant)
- **Tab Size**: 4 spaces
- **Ruler**: Visual guide at column 79
- **Trim Trailing Whitespace**: Enabled
- **Insert Final Newline**: Enabled

### Testing

- **Test Framework**: pytest
- **Test Discovery**: Automatically finds tests in `tests/` directory

## Usage

1. Open the workspace in VS Code
2. Install recommended extensions when prompted
3. The editor will automatically:
   - Format code on save
   - Show linting errors
   - Organize imports
   - Check types with mypy

## Manual Commands

You can also run these tools manually:

```bash
# Format code with Ruff
ruff format .

# Lint code with Ruff
ruff check .

# Format with Black
black .

# Sort imports with isort
isort .

# Type check with mypy
mypy .
```
