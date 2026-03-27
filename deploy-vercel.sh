#!/bin/bash

# Vercel + Railway Deployment Script
# This script helps deploy your Textile AI Management System to Vercel (frontend) and Railway (backend)

set -e

echo "🚀 Deploying Textile AI Management System to Vercel + Railway..."

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check if git is initialized
    if [ ! -d .git ]; then
        print_warning "Git repository not found. Initializing..."
        git init
        git add .
        git commit -m "Initial commit"
    fi
    
    # Check if Vercel CLI is installed
    if ! command -v vercel &> /dev/null; then
        print_status "Installing Vercel CLI..."
        npm install -g vercel
    fi
    
    print_status "Prerequisites checked ✅"
}

# Prepare frontend for Vercel
prepare_frontend() {
    print_status "Preparing frontend for Vercel..."
    
    cd frontend
    
    # Install dependencies
    npm install
    
    # Build to test
    npm run build
    
    cd ..
    print_status "Frontend prepared ✅"
}

# Prepare backend for Railway
prepare_backend() {
    print_status "Preparing backend for Railway..."
    
    cd backend
    
    # Check if requirements.txt exists
    if [ ! -f requirements.txt ]; then
        print_error "requirements.txt not found"
        exit 1
    fi
    
    cd ..
    print_status "Backend prepared ✅"
}

# Deploy to Vercel
deploy_frontend() {
    print_status "Deploying frontend to Vercel..."
    
    cd frontend
    
    # Deploy to Vercel
    vercel --prod
    
    # Get the deployed URL
    FRONTEND_URL=$(vercel ls | grep textile | head -1 | awk '{print $2}')
    
    cd ..
    
    print_status "Frontend deployed to: $FRONTEND_URL ✅"
}

# Instructions for Railway deployment
railway_instructions() {
    print_warning "Backend deployment to Railway requires manual setup:"
    echo ""
    echo "📋 STEPS FOR RAILWAY DEPLOYMENT:"
    echo "1. Go to https://railway.app"
    echo "2. Sign up with GitHub"
    echo "3. Click 'New Project' → 'Deploy from GitHub repo'"
    echo "4. Select this repository"
    echo "5. Add environment variables:"
    echo "   - DATABASE_URL=postgresql://postgres:password@localhost:5432/railway"
    echo "   - SECRET_KEY=your-secret-key-here"
    echo "6. Click 'Deploy'"
    echo ""
    echo "🔗 After deployment, you'll get a URL like: https://your-app.up.railway.app"
    echo ""
    echo "⚙️  Then update Vercel environment variable:"
    echo "   - VITE_API_BASE_URL=https://your-backend-url.up.railway.app/api"
    echo ""
}

# Main deployment function
main() {
    print_status "🚀 Starting Vercel + Railway deployment..."
    
    check_prerequisites
    prepare_frontend
    prepare_backend
    deploy_frontend
    railway_instructions
    
    print_status "🎉 Frontend deployed to Vercel!"
    print_warning "Please complete Railway deployment manually using the steps above"
}

# Handle script arguments
case "${1:-}" in
    "frontend")
        print_status "Deploying frontend only..."
        deploy_frontend
        ;;
    "backend")
        print_status "Backend deployment instructions:"
        railway_instructions
        ;;
    "prepare")
        print_status "Preparing for deployment..."
        check_prerequisites
        prepare_frontend
        prepare_backend
        ;;
    *)
        main
        ;;
esac
