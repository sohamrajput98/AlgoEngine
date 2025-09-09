# 🚀 AlgoEngine - Algorithmic Assessment Platform

A modern, full-stack coding platform with adaptive difficulty, algorithm visualization, and comprehensive problem management.

## ✨ Features

- **🎯 Adaptive Difficulty**: Problems automatically adjust to your skill level
- **📊 Algorithm Visualization**: Interactive visualizations for data structures and algorithms
- **🏆 Daily Challenges**: Curated daily coding challenges to keep skills sharp
- **🔒 Secure Code Execution**: Docker-based sandboxed code execution for Python and C++
- **📱 Modern UI**: Responsive web interface with Monaco Editor integration
- **🔐 JWT Authentication**: Secure user authentication and profile management

## 🛠️ Tech Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **MySQL** - Primary database
- **Docker** - Containerized code execution
- **JWT** - Authentication tokens
- **Alembic** - Database migrations

### Frontend
- **HTML5/CSS3/JavaScript** - Modern web technologies
- **Bootstrap 5** - Responsive UI framework
- **Monaco Editor** - VS Code-like code editor
- **Fetch API** - HTTP client for backend communication

### Infrastructure
- **Docker & Docker Compose** - Containerization and orchestration
- **Nginx** - Web server and reverse proxy

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/sohamrajput98/AlgoEngine.git
cd AlgoEngine
```

### 2. Environment Setup
```bash
# Copy environment template
cp backend/.env.example backend/.env

# Edit the .env file with your configurations
nano backend/.env
```

### 3. Start the Application
```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### 4. Initialize Database
```bash
# Run database migrations
docker-compose exec backend alembic upgrade head

# (Optional) Seed with sample problems - already included in init.sql
```

### 5. Access the Application
- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📁 Project Structure

```
AlgoEngine/
├── backend/                    # FastAPI backend
│   ├── main.py                # Main application file
│   ├── db.py                  # Database configuration
│   ├── dependencies.py        # Shared dependencies
│   ├── models/                # SQLAlchemy models
│   │   ├── user.py
│   │   ├── problem.py
│   │   ├── testcase.py
│   │   └── submission.py
│   ├── routers/               # API route handlers
│   │   ├── users.py
│   │   ├── problems.py
│   │   ├── testcases.py
│   │   └── submissions.py
│   ├── schemas/               # Pydantic schemas
│   │   ├── users.py
│   │   ├── problems.py
│   │   ├── testcases.py
│   │   └── submissions.py
│   ├── alembic/               # Database migrations
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                  # Web frontend
│   └── index.html            # Single-page application
├── runners/                   # Code execution containers
│   ├── python-runner/
│   │   ├── Dockerfile
│   │   └── run.sh
│   └── cpp-runner/
│       ├── Dockerfile
│       └── run.sh
├── docker-compose.yml         # Multi-container setup
├── init.sql                   # Database initialization
└── README.md
```

## 🔧 Development

### Backend Development
```bash
# Enter backend container
docker-compose exec backend bash

# Run tests
pytest

# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

### Adding New Languages
1. Create new runner directory: `runners/language-runner/`
2. Add Dockerfile and run.sh script
3. Update docker-compose.yml
4. Modify submission logic in backend

### Database Operations
```bash
# Reset database
docker-compose down -v
docker-compose up --build

# Backup database
docker-compose exec mysql mysqldump -u root -p aae > backup.sql

# Restore database
docker-compose exec -T mysql mysql -u root -p aae < backup.sql
```

## 🧪 Testing

### Backend Tests
```bash
# Run all tests
docker-compose exec backend pytest

# Run with coverage
docker-compose exec backend pytest --cov=.

# Run specific test file
docker-compose exec backend pytest tests/test_problems.py
```

### Frontend Testing
- Open browser dev tools and check console for errors
- Test API calls through browser network tab
- Use Postman for API testing

## 📊 API Documentation

### Authentication Endpoints
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/profile` - Get user profile
- `PUT /auth/profile` - Update user profile

### Problem Management
- `GET /problems/{id}` - Get single problem
- `PUT /problems/{id}` - Update problem (admin)
- `DELETE /problems/{id}` - Delete problem (admin)
- `GET /problems/daily-challenge/today` - Get daily challenge

### Test Cases
- `POST /problems/{id}/testcases` - Create test case (admin)
- `GET /problems/{id}/testcases` - Get public test cases
- `GET /problems/{id}/testcases/admin` - Get all test cases (admin)
- `PUT /testcases/{id}` - Update test case (admin)
- `DELETE /testcases/{id}` - Delete test case (admin)

### Code Submission
- `POST /submissions/` - Submit solution
- `GET /submissions/{id}` - Get submission details
- `GET /submissions/user/{user_id}` - Get user submissions

## 🎯 Usage Examples

### Register and Login
```javascript
// Register
const response = await fetch('http://localhost:8000/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        username: 'john_doe',
        email: 'john@example.com',
        password: 'secure123'
    })
});

// Login
const loginResponse = await fetch('http://localhost:8000/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        username_or_email: 'john_doe',
        password: 'secure123'
    })
});
const { access_token } = await loginResponse.json();
```

### Submit Solution
```javascript
const submission = await fetch('http://localhost:8000/submissions/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${access_token}`
    },
    body: JSON.stringify({
        problem_id: 1,
        code: 'def two_sum(nums, target):\n    # Your solution here\n    pass',
        language: 'python'
    })
});
```

### Create Problem (Admin)
```javascript
const problem = await fetch('http://localhost:8000/problems/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${admin_token}`
    },
    body: JSON.stringify({
        title: 'New Problem',
        description: 'Problem description...',
        concept: 'arrays',
        stars: 2,
        is_daily_candidate: true
    })
});
```

## 🔍 Problem Categories

### Data Structures
- **Arrays**: Two Sum, Best Time to Buy/Sell Stock, Contains Duplicate
- **Strings**: Valid Parentheses, Longest Substring
- **Linked Lists**: Reverse Linked List, Merge Lists
- **Trees**: Binary Tree Traversal, Maximum Depth
- **Graphs**: DFS/BFS, Shortest Path

### Algorithms
- **Sorting**: Quick Sort, Merge Sort, Heap Sort
- **Searching**: Binary Search, Linear Search
- **Dynamic Programming**: Fibonacci, Knapsack, LCS
- **Greedy**: Activity Selection, Huffman Coding
- **Backtracking**: N-Queens, Sudoku Solver

### Difficulty Levels
- ⭐ **1 Star**: Basic concepts, simple implementation
- ⭐⭐ **2 Stars**: Requires understanding of data structures
- ⭐⭐⭐ **3 Stars**: Multiple concepts, optimization needed
- ⭐⭐⭐⭐ **4 Stars**: Advanced algorithms, complex logic
- ⭐⭐⭐⭐⭐ **5 Stars**: Expert level, competitive programming

## 🎨 Visualizations Available

### Current Implementations
- **Binary Search**: Visual representation of search process
- **Two Pointers**: Array traversal with dual pointers
- **Sliding Window**: Window movement over arrays
- **Stack & Queue**: Interactive push/pop operations

### Planned Visualizations
- **Sorting Algorithms**: Bubble, Quick, Merge Sort animations
- **Tree Traversals**: DFS/BFS with step-by-step highlighting
- **Graph Algorithms**: Dijkstra's, A* pathfinding
- **Dynamic Programming**: Memoization table visualization

## 🔒 Security Features

### Code Execution Safety
- **Docker Sandboxing**: Isolated execution environment
- **Resource Limits**: CPU and memory constraints
- **Time Limits**: 10-second execution timeout
- **Network Isolation**: No external network access
- **Non-root User**: Containers run as unprivileged user

### Authentication Security
- **JWT Tokens**: Secure, stateless authentication
- **Password Hashing**: bcrypt with salt
- **Input Validation**: Pydantic schema validation
- **SQL Injection Prevention**: SQLAlchemy ORM protection

## 📈 Monitoring & Logging

### Health Checks
- `GET /health` - Application health status
- Docker health checks for all services
- Database connection monitoring

### Logging
- Structured JSON logging
- Request/response logging
- Error tracking and alerting
- Performance metrics

## 🚀 Deployment

### Production Deployment
```bash
# Clone repository on server
git clone https://github.com/sohamrajput98/AlgoEngine.git
cd AlgoEngine

# Set production environment variables
cp backend/.env.example backend/.env
# Edit .env with production values

# Deploy with Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# Setup SSL with Let's Encrypt (optional)
docker-compose exec nginx certbot --nginx -d yourdomain.com
```

### Environment Variables for Production
```bash
DATABASE_URL=mysql+pymysql://user:pass@db:3306/aae
SECRET_KEY=super-secure-production-key-minimum-32-characters
DEBUG=False
ENVIRONMENT=production
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## 🤝 Contributing

### Getting Started
1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes and test thoroughly
4. Commit changes: `git commit -m 'Add amazing feature'`
5. Push to branch: `git push origin feature/amazing-feature`
6. Create Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Write tests for new features
- Update documentation for API changes

### Code Style
```python
# Good
def calculate_max_profit(prices: list[int]) -> int:
    """Calculate maximum profit from stock prices.
    
    Args:
        prices: List of daily stock prices
        
    Returns:
        Maximum possible profit
    """
    if len(prices) < 2:
        return 0
    
    min_price = prices[0]
    max_profit = 0
    
    for price in prices[1:]:
        max_profit = max(max_profit, price - min_price)
        min_price = min(min_price, price)
    
    return max_profit
```

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error**
```bash
# Check MySQL container status
docker-compose ps mysql

# View MySQL logs
docker-compose logs mysql

# Restart database
docker-compose restart mysql
```

**Code Execution Timeout**
```bash
# Check Docker daemon
docker info

# Increase timeout in .env
CODE_EXECUTION_TIMEOUT=15

# Restart backend
docker-compose restart backend
```

**Frontend Not Loading**
```bash
# Check nginx configuration
docker-compose logs frontend

# Verify backend API
curl http://localhost:8000/health

# Check CORS settings
grep ALLOWED_ORIGINS backend/.env
```

## 📝 Changelog

### v1.0.0 (Current)
- ✅ User authentication and profiles
- ✅ Problem management system
- ✅ Code submission and execution
- ✅ Basic algorithm visualizations
- ✅ Daily challenge system
- ✅ Docker-based architecture

### Planned Features (v1.1.0)
- 🔄 Real-time contests
- 🔄 Advanced visualizations
- 🔄 Learning modules
- 🔄 Social features (following, leaderboards)
- 🔄 Mobile app
- 🔄 IDE plugins

## 🏆 Performance

### Current Metrics
- **Response Time**: < 100ms for API calls
- **Code Execution**: < 5s for most solutions
- **Concurrent Users**: Tested up to 100 simultaneous users
- **Database**: Optimized queries with proper indexing

### Optimization Features
- Database connection pooling
- Docker image caching
- Static file serving via Nginx
- Efficient algorithm implementations

## 📞 Support

### Documentation
- **API Docs**: http://localhost:8000/docs
- **GitHub Issues**: Report bugs and feature requests
- **Wiki**: Detailed guides and tutorials

### Contact
- **Email**: sohamrajput98@example.com
- **GitHub**: [@sohamrajput98](https://github.com/sohamrajput98)
- **LinkedIn**: [Soham Rajput](https://linkedin.com/in/sohamrajput98)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI**: For the excellent Python web framework
- **Monaco Editor**: For the VS Code-like editing experience
- **Bootstrap**: For the responsive UI components
- **Docker**: For containerization and security
- **MySQL**: For reliable data storage

---

**Built with ❤️ by [Soham Rajput](https://github.com/sohamrajput98)**

*AlgoEngine - Where algorithms come to life! 🚀*/` - List all problems (with filters)
- `POST /problems/` - Create new problem (admin)
- `GET /problems