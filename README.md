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

```bash
# Install dependencies
poetry install

# Run locally (Tor Browser will be installed automatically if needed)
poetry run uvicorn app.__main__:app --reload

# Or use Docker
docker-compose -f docker/docker-compose.yml up dev
```

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
