#!/bin/bash

# Script to stop development environment
set -e

echo "🛑 Stopping SaaS Contábil Development Environment..."

# Stop containers
docker compose -f ../docker-compose.dev.yml down

echo "✅ Environment stopped successfully!"
echo ""
echo "💡 To remove volumes as well:"
echo "   docker compose -f infra/docker-compose.dev.yml down -v"
