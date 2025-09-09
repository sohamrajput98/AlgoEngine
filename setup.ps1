# AlgoEngine PowerShell Setup Script
# Run this in the ROOT folder (same level as README.md)
# WITHOUT virtual environment activation

Write-Host "🚀 AlgoEngine PowerShell Setup" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

# Check if Docker is running
Write-Host "🔍 Checking Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Docker found: $dockerVersion" -ForegroundColor Green
    } else {
        throw "Docker not found"
    }
} catch {
    Write-Host "❌ Docker is not installed or not running" -ForegroundColor Red
    Write-Host "Please install Docker Desktop for Windows" -ForegroundColor Yellow
    exit 1
}

# Check if Docker Compose is available
Write-Host "🔍 Checking Docker Compose..." -ForegroundColor Yellow
try {
    $composeVersion = docker-compose --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Docker Compose found: $composeVersion" -ForegroundColor Green
    } else {
        throw "Docker Compose not found"
    }
} catch {
    Write-Host "❌ Docker Compose not found" -ForegroundColor Red
    exit 1
}

# Create .env file if it doesn't exist
if (!(Test-Path "backend\.env")) {
    Write-Host "📝 Creating .env file..." -ForegroundColor Yellow
    if (Test-Path "backend\.env.example") {
        Copy-Item "backend\.env.example" "backend\.env"
        Write-Host "✅ Created .env from example" -ForegroundColor Green
    } else {
        Write-Host "⚠️  .env.example not found, creating basic .env" -ForegroundColor Yellow
        $envContent = @"
DATABASE_URL=mysql+pymysql://algouser:algopassword@localhost:3306/aae
SECRET_KEY=your-super-secret-key-change-in-production-minimum-32-chars
DEBUG=True
ENVIRONMENT=development
"@
        $envContent | Out-File -FilePath "backend\.env" -Encoding UTF8
        Write-Host "✅ Created basic .env file" -ForegroundColor Green
    }
} else {
    Write-Host "✅ .env file already exists" -ForegroundColor Green
}

# Create directories
Write-Host "📁 Creating directories..." -ForegroundColor Yellow
$directories = @("backend\schemas", "frontend", "runners\python-runner", "runners\cpp-runner")
foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✅ Created directory: $dir" -ForegroundColor Green
    }
}

# Stop any running containers
Write-Host "🛑 Stopping existing containers..." -ForegroundColor Yellow
docker-compose down -v 2>$null

# Build and start services
Write-Host "🔨 Building and starting services..." -ForegroundColor Yellow
Write-Host "This may take a few minutes on first run..." -ForegroundColor Yellow

docker-compose build --no-cache
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker build failed" -ForegroundColor Red
    exit 1
}

Write-Host "🚀 Starting services..." -ForegroundColor Yellow
docker-compose up -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to start services" -ForegroundColor Red
    exit 1
}

# Wait for services
Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Check service health
Write-Host "🔍 Checking services..." -ForegroundColor Yellow

# Check MySQL
$mysqlStatus = docker-compose ps mysql 2>$null
if ($mysqlStatus -match "Up") {
    Write-Host "✅ MySQL is running" -ForegroundColor Green
} else {
    Write-Host "❌ MySQL failed to start" -ForegroundColor Red
    Write-Host "MySQL logs:" -ForegroundColor Yellow
    docker-compose logs mysql
}

# Check Backend
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 10 2>$null
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Backend API is running" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Backend API not responding" -ForegroundColor Red
    Write-Host "Backend logs:" -ForegroundColor Yellow
    docker-compose logs backend
}

# Check Frontend
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8080" -TimeoutSec 10 2>$null
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Frontend is running" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Frontend not responding" -ForegroundColor Red
    Write-Host "Frontend logs:" -ForegroundColor Yellow
    docker-compose logs frontend
}

Write-Host ""
Write-Host "🎉 AlgoEngine setup complete!" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host ""
Write-Host "📱 Access your application:" -ForegroundColor Cyan
Write-Host "   Frontend:  http://localhost:8080" -ForegroundColor White
Write-Host "   Backend:   http://localhost:8000" -ForegroundColor White
Write-Host "   API Docs:  http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "🔧 Useful commands:" -ForegroundColor Cyan
Write-Host "   View logs:     docker-compose logs -f [service]" -ForegroundColor White
Write-Host "   Stop:          docker-compose down" -ForegroundColor White
Write-Host "   Restart:       docker-compose restart [service]" -ForegroundColor White
Write-Host ""
Write-Host "Happy coding! 🚀" -ForegroundColor Green