#!/bin/bash

# Script to start development environment
set -e

echo "🚀 Starting SaaS Contábil Development Environment..."

# Load environment variables
if [ -f ../../.env ]; then
    export $(cat ../../.env | grep -v '^#' | xargs)
fi

# Build and start containers
echo "📦 Building and starting Docker containers..."
docker compose -f ../docker-compose.dev.yml up --build -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Show status
echo "📊 Service Status:"
docker compose -f ../docker-compose.dev.yml ps

echo ""
echo "✅ Environment is up and running!"
echo ""
echo "🌐 Access URLs:"
echo "   - Frontend:  http://localhost:3000"
echo "   - API:       http://localhost:8000"
echo "   - API Docs:  http://localhost:8000/docs"
echo "   - Nginx:     http://localhost"
echo "   - PostgreSQL: localhost:5432"
echo ""
echo "📝 Logs:"
echo "   docker compose -f infra/docker-compose.dev.yml logs -f"
echo ""
echo "🛑 To stop:"
echo "   ./infra/scripts/dev-down.sh"
