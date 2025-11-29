# core-scraper-service

```
████████╗ ██████╗ ██████╗       ███╗   ██╗███████╗████████╗██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗
╚══██╔══╝██╔═══██╗██╔══██╗      ████╗  ██║██╔════╝╚══██╔══╝██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝
   ██║   ██║   ██║██████╔╝█████╗██╔██╗ ██║█████╗     ██║   ██║ █╗ ██║██║   ██║██████╔╝█████╔╝
   ██║   ██║   ██║██╔══██╗╚════╝██║╚██╗██║██╔══╝     ██║   ██║███╗██║██║   ██║██╔══██╗██╔═██╗
   ██║   ╚██████╔╝██║  ██║      ██║ ╚████║███████╗   ██║   ╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗
   ╚═╝    ╚═════╝ ╚═╝  ╚═╝      ╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
 ```

## Setup

### Automatic Installation

**Tor Browser is installed automatically** when not found. No manual
configuration needed!

The service will:
1. Detect Tor Browser in common locations
2. Automatically download and install if not found (Linux only)
3. Use the installed version for scraping

### Environment Variables (Optional)

Only needed if you want to override defaults:

```bash
TOR_BROWSER_PATH=~/tor-browser  # Custom path
TOR_DATA_DIR=/tmp/tor-data      # Custom data directory
DATABASE_URL=sqlite:///./sql_app.db
SCOPE=development
```

**Note:** On macOS, Tor Browser must be installed manually from
[torproject.org](https://www.torproject.org/download/).

## Development

### Dependencies Management

**All dependencies are managed through Poetry** (`pyproject.toml` and `poetry.lock`).

```bash
# Install dependencies
poetry install

# Install with development dependencies
poetry install --with code-quality,testing

# Update dependencies
poetry update

# Add a new dependency
poetry add package-name

# Add a development dependency
poetry add --group code-quality package-name
```

### Running Locally

```bash
# Run locally (Tor Browser will be installed automatically if needed)
poetry run uvicorn app.__main__:app --reload

# Or use Docker
docker-compose -f docker/docker-compose.yml up dev
```

### Lambda Deployment

For AWS Lambda deployment, the project uses Poetry directly:
- `serverless.yml` is configured with `usePoetry: true`
- Dockerfiles use Poetry to install dependencies
- All dependencies are managed through `pyproject.toml` and `poetry.lock`

## Commit Style

- ⚙️ FEATURE
- 📝 PEP8
- 📌 ISSUE
- 🪲 BUG
- 📘 DOCS
- 📦 PyPI
- ❤️️ TEST
- ⬆️ CI/CD
- ⚠️ SECURITY

## License

This project is licensed under the terms of the GPL-3.0 license.
