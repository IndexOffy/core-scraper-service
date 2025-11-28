#!/bin/bash
# Helper script to run Docker containers for local testing

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Parse command line arguments
MODE=${1:-dev}
PORT=${2:-8000}

case $MODE in
    lambda)
        print_info "Building Lambda simulation environment..."
        docker build -f docker/Dockerfile.lambda -t core-scraper-lambda .

        print_info "Starting Lambda simulation on port 9000..."
        docker run -d --name core-scraper-lambda \
            -p 9000:8080 \
            -e SCOPE=production \
            -e AWS_LAMBDA_FUNCTION_NAME=local-test \
            core-scraper-lambda

        print_info "Lambda simulation is running at http://localhost:9000"
        print_info "Use 'docker logs -f core-scraper-lambda' to view logs"
        ;;

    dev)
        print_info "Building development environment..."
        docker build -f docker/Dockerfile.dev -t core-scraper-dev .

        print_info "Starting development server on port $PORT..."
        docker run -d --name core-scraper-dev \
            -p $PORT:8000 \
            -v "$(pwd)/app:/app/app" \
            -v "$(pwd)/lambda_handler.py:/app/lambda_handler.py" \
            -e SCOPE=development \
            -e PYTHONPATH=/app \
            core-scraper-dev

        print_info "Development server is running at http://localhost:$PORT"
        print_info "Use 'docker logs -f core-scraper-dev' to view logs"
        print_info "Use 'docker stop core-scraper-dev' to stop"
        ;;

    tor)
        print_info "Building Tor Browser environment (this may take a while)..."
        docker build -f docker/Dockerfile.tor -t core-scraper-tor .

        print_info "Starting Tor Browser environment on port 8001..."
        docker run -d --name core-scraper-tor \
            -p 8001:8000 \
            -e SCOPE=production \
            -e TOR_BROWSER_PATH=/opt/tor-browser \
            -e TOR_DATA_DIR=/tmp/tor-data \
            core-scraper-tor

        print_info "Tor Browser environment is running at http://localhost:8001"
        print_info "Use 'docker logs -f core-scraper-tor' to view logs"
        ;;

    stop)
        print_info "Stopping all containers..."
        docker stop core-scraper-lambda core-scraper-dev core-scraper-tor 2>/dev/null || true
        print_info "Containers stopped"
        ;;

    clean)
        print_info "Stopping and removing all containers..."
        docker stop core-scraper-lambda core-scraper-dev core-scraper-tor 2>/dev/null || true
        docker rm core-scraper-lambda core-scraper-dev core-scraper-tor 2>/dev/null || true
        print_info "Containers cleaned"
        ;;

    logs)
        CONTAINER=${2:-dev}
        print_info "Showing logs for core-scraper-$CONTAINER..."
        docker logs -f core-scraper-$CONTAINER
        ;;

    *)
        echo "Usage: $0 {lambda|dev|tor|stop|clean|logs} [port]"
        echo ""
        echo "Commands:"
        echo "  lambda  - Run Lambda simulation environment (port 9000)"
        echo "  dev     - Run development environment with hot-reload (port 8000)"
        echo "  tor     - Run Tor Browser environment (port 8001)"
        echo "  stop    - Stop all running containers"
        echo "  clean   - Stop and remove all containers"
        echo "  logs    - Show logs for a container (default: dev)"
        echo ""
        echo "Examples:"
        echo "  $0 dev          # Start dev environment on port 8000"
        echo "  $0 dev 3000     # Start dev environment on port 3000"
        echo "  $0 logs lambda  # Show logs for lambda container"
        exit 1
        ;;
esac
