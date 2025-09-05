# Docker E2E Application

A containerized microservices application built with FastAPI, PostgreSQL, Redis, and Nginx. This project demonstrates modern application architecture patterns including API development, database management, caching strategies, and containerized deployment.

## Architecture Overview

The application follows a multi-tier architecture pattern with the following components:

- **API Layer**: FastAPI application providing RESTful endpoints
- **Database Layer**: PostgreSQL for persistent data storage
- **Caching Layer**: Redis for session management and performance optimization
- **Proxy Layer**: Nginx as reverse proxy and load balancer
- **Testing Layer**: Automated health checks and integration tests

## Technology Stack

### Backend
- **FastAPI 0.115.8** - Modern Python web framework for building APIs
- **SQLAlchemy 2.0.39** - Python SQL toolkit and Object-Relational Mapping
- **Alembic 1.14.0** - Database migration tool for SQLAlchemy
- **Pydantic 2.10.6** - Data validation using Python type annotations

### Database & Caching
- **PostgreSQL 16** - Primary database for persistent storage
- **Redis 7-alpine** - In-memory data store for caching and sessions

### Infrastructure
- **Docker & Docker Compose** - Containerization and orchestration
- **Nginx 1.27** - Reverse proxy and static file serving
- **Uvicorn 0.34.0** - ASGI server for running FastAPI applications

## Project Structure

```
docker-e2e/
├── app/                    # Application source code
│   ├── main.py            # FastAPI application entry point
│   ├── models.py          # SQLAlchemy database models
│   ├── schemas.py         # Pydantic data models
│   ├── crud.py            # Database operations
│   ├── db.py              # Database connection configuration
│   ├── requirements.txt   # Python dependencies
│   └── alembic/           # Database migration files
│       └── env.py         # Alembic configuration
├── nginx/
│   └── nginx.conf         # Nginx reverse proxy configuration
├── tests/
│   └── test_health.py     # Health check tests
├── docker-compose.yml     # Multi-container application definition
├── Dockerfile             # Container image build instructions
└── Makefile              # Development automation scripts
```

## Prerequisites

Before running this application, ensure you have the following installed:

- Docker (version 20.0 or higher)
- Docker Compose (version 2.0 or higher)
- Make (for using Makefile commands)

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd docker-e2e
```

### 2. Environment Configuration

Create a `.env` file based on the provided example:

```bash
cp .env.example .env
```

Edit the `.env` file with your preferred configuration:

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/postgres
REDIS_HOST=redis
API_URL=http://localhost
```

### 3. Start the Application

```bash
# Using Make (recommended)
make up

# Or using Docker Compose directly
docker compose up -d
```

### 4. Verify Installation

Check that all services are running:

```bash
make ps
# or
docker compose ps
```

Test the application:

```bash
curl http://localhost/health
```

Expected response:
```json
{"status":"ok"}
```

## API Endpoints

The application provides the following RESTful endpoints:

### Health Check
- **GET** `/health` - Returns application health status

### User Management
- **POST** `/users` - Create a new user
- **GET** `/users` - Retrieve all users

### Utility
- **POST** `/counter` - Increment and return hit counter (Redis-based)

### Example API Usage

Create a new user:
```bash
curl -X POST http://localhost/users \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "name": "John Doe"}'
```

Retrieve all users:
```bash
curl http://localhost/users
```

## Development Workflow

### Available Make Commands

The project includes a Makefile with common development tasks:

```bash
make up           # Start all services
make down         # Stop all services
make logs         # View application logs
make ps           # Show service status
make bash         # Access API container shell
make migrate      # Run database migrations
make test         # Execute health checks
make ci-test      # Run full CI test suite
make lint         # Run code quality checks
make format       # Format code with black and isort
make security-check # Run security vulnerability checks
make scan         # Security scan of Docker images
make build        # Build Docker images
make clean        # Clean up containers and images
```

## Continuous Integration

The project includes a comprehensive CI/CD pipeline using GitHub Actions with the following features:

### Automated Testing
- **Code Quality**: Linting with flake8, formatting checks with black and isort
- **Unit Tests**: Automated testing with pytest
- **Integration Tests**: End-to-end testing of all services
- **Performance Tests**: Load testing with Apache Bench
- **Security Scans**: Vulnerability scanning with Trivy and CodeQL

### Deployment Pipeline
- **Docker Image Building**: Automated image builds and pushes to GitHub Container Registry
- **Staging Deployment**: Automated deployment to staging environment
- **Dependency Management**: Automated dependency updates with Dependabot

### Security Monitoring
- **Daily Security Scans**: Automated vulnerability scanning
- **Dependency Audits**: Regular security audits of Python packages
- **Container Security**: Runtime security scanning of Docker images

### Workflow Triggers
- **Push to main/develop**: Full CI/CD pipeline execution
- **Pull Requests**: Code quality checks and integration tests
- **Scheduled**: Daily security scans and dependency updates
- **Manual**: On-demand workflow execution

### Database Migrations

The application uses Alembic for database schema management:

```bash
# Generate a new migration after model changes
make migrate

# Or run manually
docker compose exec api alembic revision --autogenerate -m "description"
docker compose exec api alembic upgrade head
```

### Running Tests

Execute the test suite:

```bash
make test
```

For more comprehensive testing:

```bash
# Install test dependencies and run pytest
docker compose exec api pip install pytest requests
docker compose exec api pytest tests/
```

## Configuration

### Environment Variables

The application supports the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+psycopg://postgres:postgres@db:5432/postgres` |
| `REDIS_HOST` | Redis server hostname | `redis` |
| `API_URL` | API base URL for testing | `http://localhost` |
| `POSTGRES_USER` | Database username | `postgres` |
| `POSTGRES_PASSWORD` | Database password | `postgres` |
| `POSTGRES_DB` | Database name | `postgres` |

### Service Ports

The following ports are exposed:

- **80**: Nginx reverse proxy (main application access)
- **5432**: PostgreSQL database
- **6379**: Redis cache

## Deployment

### Production Considerations

For production deployment, consider the following modifications:

1. **Security**: Use secrets management instead of environment variables
2. **SSL/TLS**: Configure SSL certificates in Nginx
3. **Scaling**: Use Docker Swarm or Kubernetes for orchestration
4. **Monitoring**: Add logging and metrics collection
5. **Backup**: Implement database backup strategies

### Docker Image Building

The application uses a multi-stage Dockerfile for optimized image size:

```bash
# Build the image manually
docker build -t docker-e2e-api .

# Or let Docker Compose handle it
docker compose build
```

## Monitoring and Logging

### Application Logs

View real-time logs:

```bash
make logs
# or
docker compose logs -f
```

View logs for specific services:

```bash
docker compose logs -f api
docker compose logs -f nginx
docker compose logs -f db
```

### Health Monitoring

The application includes health check endpoints for monitoring:

- Application health: `GET /health`
- Database connectivity is verified through the ORM
- Redis connectivity is tested via the counter endpoint

## Troubleshooting

### Common Issues

**Port Conflicts**
If you encounter port binding errors, ensure ports 80, 5432, and 6379 are not in use:

```bash
# Check port usage
netstat -tulpn | grep :80
netstat -tulpn | grep :5432
netstat -tulpn | grep :6379

# Stop conflicting services
sudo systemctl stop nginx  # if system nginx is running
```

**Database Connection Issues**
Verify database service is running and accessible:

```bash
docker compose exec db psql -U postgres -d postgres -c "SELECT 1;"
```

**Import Errors**
If you encounter Python import errors, rebuild the API container:

```bash
docker compose build api
docker compose up -d api
```

### Debugging

Access the API container for debugging:

```bash
make bash
# or
docker compose exec api bash
```

Check service connectivity from within containers:

```bash
# Test database connection
docker compose exec api python -c "from db import engine; print(engine.execute('SELECT 1').scalar())"

# Test Redis connection
docker compose exec api python -c "import redis; r=redis.Redis(host='redis'); print(r.ping())"
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`make test`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Style

The project follows Python PEP 8 style guidelines. Consider using tools like `black` and `flake8` for code formatting and linting.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FastAPI community for excellent documentation and examples
- SQLAlchemy team for the robust ORM framework
- Docker community for containerization best practices
