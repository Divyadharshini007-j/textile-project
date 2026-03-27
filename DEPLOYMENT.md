# 🚀 Deployment Guide for Textile AI Management System

## Quick Deployment Options

### Option 1: Local Development (Easiest)
```bash
# Clone and run locally
git clone <your-repo>
cd textile_ai_project
./deploy.sh dev
```

### Option 2: Production Deployment (Recommended)
```bash
# Deploy to production
git clone <your-repo>
cd textile_ai_project
cp .env.example .env
# Edit .env with your values
./deploy.sh prod
```

### Option 3: Manual Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose -f docker-compose.prod.yml up -d
```

## 🌐 Cloud Deployment Options

### Heroku (Free Tier Available)
1. Install Heroku CLI
2. Create app: `heroku create your-app-name`
3. Set environment variables
4. Deploy: `git push heroku main`

### AWS/Google Cloud/Azure
1. Create VM instance (2GB RAM minimum)
2. Install Docker
3. Clone repository
4. Run deployment script

### VPS Providers (DigitalOcean, Vultr, Linode)
1. Create VPS (2GB RAM, 1 CPU minimum)
2. Point domain to VPS IP
3. Follow manual deployment steps

## 📋 Prerequisites

### Minimum Requirements
- **RAM**: 2GB (4GB recommended)
- **Storage**: 20GB (50GB recommended)
- **CPU**: 1 core (2 cores recommended)
- **OS**: Ubuntu 20.04+ or CentOS 8+

### Software Needed
- Docker & Docker Compose
- Git
- Domain name (optional but recommended)

## 🔧 Configuration Steps

### 1. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit with your values
nano .env
```

### 2. SSL Certificate (Recommended)
```bash
# Using Let's Encrypt (for production)
sudo apt install certbot
sudo certbot certonly --standalone -d your-domain.com
```

### 3. Database Setup
```bash
# The deployment script handles this automatically
# Manual setup if needed:
docker-compose exec db psql -U textile_user -d textile_db
```

## 🌍 Access Your Application

After deployment, your application will be available at:
- **Frontend**: http://your-domain.com (or http://localhost)
- **Backend API**: http://your-domain.com/api
- **API Docs**: http://your-domain.com/docs

### Default Login
- **Username**: admin
- **Password**: admin123

## 🔒 Security Checklist

### ✅ Must-Do Before Production
1. **Change default passwords** in .env file
2. **Set up SSL certificates**
3. **Configure firewall** (ports 80, 443 only)
4. **Update all packages**
5. **Set up database backups**
6. **Monitor logs regularly**

### 🔐 Recommended Security Measures
- Use strong SECRET_KEY (generate with: `openssl rand -hex 32`)
- Enable rate limiting (included in nginx config)
- Set up log monitoring
- Regular security updates
- Backup strategy implementation

## 📊 Monitoring & Maintenance

### Health Checks
```bash
# Check all services
./deploy.sh health

# View logs
./deploy.sh logs
```

### Database Backups
```bash
# Manual backup
docker-compose exec db pg_dump -U textile_user textile_db > backup.sql

# Automated backup (add to crontab)
0 2 * * * /path/to/backup-script.sh
```

### Updates
```bash
# Update application
git pull
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

## 🐛 Troubleshooting

### Common Issues

#### Application Not Starting
```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Check ports
netstat -tlnp | grep :80
netstat -tlnp | grep :8000
```

#### Database Connection Issues
```bash
# Check database status
docker-compose exec db pg_isready

# Test connection
docker-compose exec backend python -c "from app.db.base import engine; print('DB OK' if engine else 'DB Failed')"
```

#### SSL Certificate Issues
```bash
# Check certificate
openssl x509 -in /etc/nginx/ssl/cert.pem -text -noout

# Test SSL configuration
nginx -t
```

## 📈 Performance Optimization

### Database Optimization
- Add indexes to frequently queried columns
- Use connection pooling
- Optimize queries

### Frontend Optimization
- Enable gzip compression (included)
- Use CDN for static assets
- Implement caching

### Backend Optimization
- Use Redis for caching
- Implement API rate limiting
- Optimize database queries

## 🆘 Support

### Getting Help
1. Check the logs: `./deploy.sh logs`
2. Review this documentation
3. Check API documentation at `/docs`
4. Verify environment variables

### Emergency Recovery
```bash
# Stop all services
./deploy.sh stop

# Restore from backup
docker-compose exec -T db psql -U textile_user textile_db < backup.sql

# Restart services
./deploy.sh prod
```

---

## 🎉 You're Ready!

Your Textile AI Management System is now deployed and ready for production use!

For additional help, check the main README.md or open an issue in the repository.
