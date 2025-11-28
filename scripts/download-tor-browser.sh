#!/bin/bash
# Download and extract Tor Browser for Lambda deployment

set -e

TOR_BROWSER_VERSION="${TOR_BROWSER_VERSION:-13.0.12}"
TOR_BROWSER_LANG="${TOR_BROWSER_LANG:-en-US}"
OUTPUT_DIR="${1:-/opt/tor-browser}"

echo "Downloading Tor Browser ${TOR_BROWSER_VERSION}..."

mkdir -p "${OUTPUT_DIR}"

# Download Tor Browser
TMP_FILE="/tmp/tor-browser-${TOR_BROWSER_VERSION}.tar.xz"
wget -q -O "${TMP_FILE}" \
    "https://www.torproject.org/dist/torbrowser/${TOR_BROWSER_VERSION}/tor-browser-linux64-${TOR_BROWSER_VERSION}_${TOR_BROWSER_LANG}.tar.xz" || {
    echo "Failed to download Tor Browser"
    exit 1
}

# Extract
echo "Extracting Tor Browser..."
tar -xf "${TMP_FILE}" -C "${OUTPUT_DIR}" --strip-components=1

# Make executable
chmod +x "${OUTPUT_DIR}/Browser/firefox"

# Cleanup
rm -f "${TMP_FILE}"

echo "Tor Browser installed to ${OUTPUT_DIR}"
