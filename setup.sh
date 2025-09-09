#!/bin/bash

# AlgoEngine Setup Script
# This script sets up the complete AlgoEngine platform

set -e  # Exit on any error

echo "🚀 Welcome to AlgoEngine Setup!"
echo "=================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create .env file if it doesn't exist
if [ ! -f "backend/.env" ]; then
    echo "📝 Creating environment file..."
    cp backend/.env.example backend/.env
    echo "✅ Environment file created at backend/.env"
    echo "📋 You can edit it later if needed"
else
    echo "✅ Environment file already exists"
fi

# Create necessary directories
echo "📁 Creating project directories..."
mkdir -p backend/models backend/routers backend/schemas backend/alembic
mkdir -p frontend runners/python-runner runners/cpp-runner
echo "✅ Directories created"

# Make scripts executable
chmod +x runners/python-runner/run.sh 2>/dev/null || true
chmod +x runners/cpp-runner/run.sh 2>/dev/null || true

# Build and start services
echo "🔨 Building and starting services..."
echo "This may take a few minutes on first run..."

docker-compose down -v 2>/dev/null || true  # Clean up any existing containers
docker-compose build --no-cache

echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Check if services are running
echo "🔍 Checking service health..."

# Check MySQL
if docker-compose ps mysql | grep -q "Up"; then
    echo "✅ MySQL is running"
else
    echo "❌ MySQL failed to start"
    docker-compose logs mysql
    exit 1
fi

# Check Backend
if curl -f http://localhost:8000/health &>/dev/null; then
    echo "✅ Backend API is running"
else
    echo "❌ Backend API failed to start"
    docker-compose logs backend
    exit 1
fi

# Check Frontend
if curl -f http://localhost:8080 &>/dev/null; then
    echo "✅ Frontend is running"
else
    echo "❌ Frontend failed to start"
    docker-compose logs frontend
fi

echo ""
echo "🎉 AlgoEngine setup complete!"
echo "=================================="
echo ""
echo "📱 Access your application:"
echo "   Frontend:  http://localhost:8080"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "🔧 Useful commands:"
echo "   View logs:     docker-compose logs -f [service]"
echo "   Stop:          docker-compose down"
echo "   Restart:       docker-compose restart [service]"
echo "   Shell access:  docker-compose exec [service] bash"
echo ""
echo "📚 Sample problems are already loaded!"
echo "💡 Create an account and start coding!"
echo ""
echo "🐛 If you encounter issues, check:"
echo "   1. Docker is running"
echo "   2. Ports 3306, 8000, 8080 are not in use"
echo "   3. Check logs with: docker-compose logs"
echo ""
echo "Happy coding! 🚀"