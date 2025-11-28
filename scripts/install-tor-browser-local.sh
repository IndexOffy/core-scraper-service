#!/bin/bash
# Install Tor Browser locally for development

set -e

TOR_BROWSER_VERSION="${TOR_BROWSER_VERSION:-13.0.12}"
TOR_BROWSER_LANG="${TOR_BROWSER_LANG:-en-US}"

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    ARCH="x86_64"
    EXT="dmg"
    INSTALL_DIR="${HOME}/tor-browser"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    ARCH="x86_64"
    EXT="tar.xz"
    INSTALL_DIR="${HOME}/tor-browser"
else
    echo "Unsupported OS: $OSTYPE"
    exit 1
fi

echo "Installing Tor Browser ${TOR_BROWSER_VERSION} for ${OS}..."

mkdir -p "${INSTALL_DIR}"

if [[ "$OS" == "macos" ]]; then
    echo "macOS installation requires manual steps:"
    echo "1. Download from: https://www.torproject.org/download/"
    echo "2. Extract to: ${INSTALL_DIR}"
    echo "3. Set TOR_BROWSER_PATH=${INSTALL_DIR}/Tor Browser.app/Contents/MacOS"
    exit 0
fi

# Download Tor Browser for Linux
TMP_FILE="/tmp/tor-browser-${TOR_BROWSER_VERSION}.tar.xz"
echo "Downloading Tor Browser..."
wget -q -O "${TMP_FILE}" \
    "https://www.torproject.org/dist/torbrowser/${TOR_BROWSER_VERSION}/tor-browser-linux64-${TOR_BROWSER_VERSION}_${TOR_BROWSER_LANG}.tar.xz" || {
    echo "Failed to download Tor Browser"
    exit 1
}

# Extract
echo "Extracting Tor Browser..."
tar -xf "${TMP_FILE}" -C "${INSTALL_DIR}" --strip-components=1

# Make executable
chmod +x "${INSTALL_DIR}/Browser/firefox"

# Cleanup
rm -f "${TMP_FILE}"

echo "Tor Browser installed to ${INSTALL_DIR}"
echo ""
echo "Add to your .env file:"
echo "TOR_BROWSER_PATH=${INSTALL_DIR}"

