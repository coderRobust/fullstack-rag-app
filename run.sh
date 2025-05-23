#!/bin/bash

echo "🔍 Checking .env..."
if [ ! -f .env ]; then
  echo "❌ ERROR: .env file is missing in the root directory."
  exit 1
fi

echo "✅ .env file found."

echo "🐳 Building and starting all Docker containers..."
docker-compose -f docker/docker-compose.yml up --build -d

echo "⏳ Waiting for services to be healthy..."
sleep 10

echo "📦 Services running:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo "🌐 Access your app at:"
echo "Frontend: http://localhost:3000"
echo "Backend API Docs: http://localhost:8000/docs"

echo "📜 To follow logs: docker-compose -f docker/docker-compose.yml logs -f"
