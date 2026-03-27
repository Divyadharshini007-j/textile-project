# Textile AI Management System

A comprehensive textile industry management system with AI-powered price predictions, inventory management, and worker hiring portal.

## Features

- 🏭 **Inventory Management**: Track yarn stocks, purchases, and sales
- 🤖 **AI Price Predictions**: 3-month yarn price forecasting using machine learning
- 👥 **Worker Hiring Portal**: Complete job posting and application system
- 📊 **Business Dashboard**: Real-time KPIs and financial insights
- 💰 **Financial Management**: Sales, purchases, expenses tracking
- 📋 **Customer & Supplier Management**: Complete CRM functionality

## Tech Stack

### Backend
- **FastAPI** (Python)
- **PostgreSQL** Database
- **SQLAlchemy** ORM
- **Machine Learning**: scikit-learn for price predictions
- **JWT Authentication**

### Frontend
- **React.js** with Material-UI
- **Vite** for fast development
- **Axios** for API communication
- **Formik** & Yup for form handling

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd textile_ai_project
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Database Setup**
```bash
# Create PostgreSQL database
createdb textile_db

# Run migrations (if available)
# Or create tables using SQLAlchemy models
```

4. **Environment Configuration**
```bash
# Create .env file in backend/
DATABASE_URL=postgresql://username:password@localhost/textile_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. **Start Backend**
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

6. **Frontend Setup**
```bash
cd frontend
npm install
npm run dev
```

7. **Access Application**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Default Login
- Username: `admin`
- Password: `admin123`

## Deployment Options

### Option 1: Docker Deployment (Recommended)

1. **Build Docker Images**
```bash
# Backend
docker build -t textile-backend ./backend

# Frontend  
docker build -t textile-frontend ./frontend
```

2. **Use Docker Compose**
```bash
docker-compose up -d
```

### Option 2: Cloud Deployment

#### Heroku
```bash
# Install Heroku CLI
heroku create your-app-name

# Set environment variables
heroku config:set DATABASE_URL=your-production-db-url

# Deploy
git push heroku main
```

#### AWS/Google Cloud/Azure
- Use the provided Dockerfile configurations
- Set up managed PostgreSQL database
- Configure environment variables
- Deploy using container services

### Option 3: VPS Deployment

1. **Server Setup**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3 python3-pip nodejs npm postgresql -y

# Install Docker (optional but recommended)
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

2. **Application Deployment**
```bash
# Clone repository
git clone <repository-url>
cd textile_ai_project

# Use Docker Compose
docker-compose -f docker-compose.prod.yml up -d
```

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/textile_db
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]
```

### Frontend (.env)
```env
VITE_API_BASE_URL=https://your-api-domain.com/api
```

## Database Schema

The application uses the following main tables:
- `users` - Authentication and user management
- `customers` - Customer information
- `suppliers` - Supplier details
- `products` - Product catalog
- `inventory` - Stock management
- `purchases` - Purchase orders
- `sales` - Sales records
- `expenses` - Business expenses
- `workers` - Worker management
- `jobs` - Job postings
- `applications` - Job applications

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Monitoring & Logging

### Application Logs
```bash
# Backend logs
docker logs textile-backend

# Frontend logs  
docker logs textile-frontend
```

### Health Checks
- Backend Health: http://localhost:8000/health
- Frontend Health: http://localhost:3000

## Security Considerations

1. **Change default passwords** before production
2. **Use HTTPS** in production
3. **Validate all inputs** (already implemented)
4. **Use environment variables** for sensitive data
5. **Regular updates** of dependencies
6. **Database backups** configured

## Performance Optimization

1. **Database indexing** on frequently queried columns
2. **API response caching** where appropriate
3. **Frontend code splitting** for faster loads
4. **Image optimization** for product images
5. **CDN** for static assets in production

## Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review the logs for error messages
3. Verify database connections
4. Ensure all environment variables are set

## License

This project is licensed under the MIT License.
