#!/bin/bash

# Script to view logs from all services
set -e

echo "📋 Viewing logs from all services..."
echo "Press Ctrl+C to exit"
echo ""

docker compose -f ../docker-compose.dev.yml logs -f
