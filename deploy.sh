#!/bin/bash

# Textile AI Management System Deployment Script
# This script helps deploy the application to production

set -e

echo "🚀 Starting Textile AI Management System Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_status "Docker and Docker Compose are installed"
}

# Check if .env file exists
check_env_file() {
    if [ ! -f .env ]; then
        print_warning ".env file not found. Creating from template..."
        cp .env.example .env
        print_warning "Please edit .env file with your production values before continuing!"
        print_warning "Especially change SECRET_KEY and DB_PASSWORD!"
        read -p "Press Enter after editing .env file..."
    fi
}

# Build and start services
deploy_application() {
    print_status "Building and starting application..."
    
    # Stop existing services
    docker-compose -f docker-compose.prod.yml down
    
    # Build images
    print_status "Building Docker images..."
    docker-compose -f docker-compose.prod.yml build
    
    # Start services
    print_status "Starting services..."
    docker-compose -f docker-compose.prod.yml up -d
    
    # Wait for services to be ready
    print_status "Waiting for services to start..."
    sleep 30
}

# Check service health
check_health() {
    print_status "Checking service health..."
    
    # Check backend
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_status "✅ Backend is healthy"
    else
        print_error "❌ Backend is not responding"
        return 1
    fi
    
    # Check frontend
    if curl -f http://localhost > /dev/null 2>&1; then
        print_status "✅ Frontend is healthy"
    else
        print_error "❌ Frontend is not responding"
        return 1
    fi
}

# Database setup
setup_database() {
    print_status "Setting up database..."
    
    # Wait for database to be ready
    docker-compose -f docker-compose.prod.yml exec -T db pg_isready -U textile_user -d textile_db
    
    # Run database migrations (if you have them)
    # docker-compose -f docker-compose.prod.yml exec -T backend alembic upgrade head
    
    print_status "Database is ready"
}

# Show deployment info
show_deployment_info() {
    print_status "🎉 Deployment completed successfully!"
    echo ""
    echo "📋 Deployment Information:"
    echo "🌐 Frontend: http://localhost"
    echo "🔧 Backend API: http://localhost:8000"
    echo "📚 API Documentation: http://localhost:8000/docs"
    echo ""
    echo "👤 Default Login:"
    echo "   Username: admin"
    echo "   Password: admin123"
    echo ""
    echo "🔧 Useful Commands:"
    echo "   View logs: docker-compose -f docker-compose.prod.yml logs -f"
    echo "   Stop services: docker-compose -f docker-compose.prod.yml down"
    echo "   Restart services: docker-compose -f docker-compose.prod.yml restart"
    echo ""
    print_warning "Remember to:"
    echo "   1. Change default passwords"
    echo "   2. Set up SSL certificates"
    echo "   3. Configure domain name"
    echo "   4. Set up database backups"
}

# Main deployment function
main() {
    print_status "🚀 Starting deployment of Textile AI Management System..."
    
    check_docker
    check_env_file
    deploy_application
    setup_database
    check_health
    show_deployment_info
}

# Handle script arguments
case "${1:-}" in
    "dev")
        print_status "Starting in development mode..."
        docker-compose up -d
        ;;
    "prod")
        main
        ;;
    "stop")
        print_status "Stopping services..."
        docker-compose -f docker-compose.prod.yml down
        ;;
    "logs")
        docker-compose -f docker-compose.prod.yml logs -f
        ;;
    "health")
        check_health
        ;;
    *)
        echo "Usage: $0 {dev|prod|stop|logs|health}"
        echo ""
        echo "  dev   - Start in development mode"
        echo "  prod  - Deploy to production"
        echo "  stop  - Stop all services"
        echo "  logs  - Show logs"
        echo "  health - Check service health"
        exit 1
        ;;
esac
