# 🚀 Vercel Deployment Guide

## 📋 Overview

This guide will help you deploy your Textile AI Management System with:
- **Frontend** on Vercel (React app)
- **Backend** on Railway (Python FastAPI)

## 🎯 Why This Setup?

### ✅ Vercel (Frontend)
- Free hosting for React apps
- Automatic deployments from Git
- Global CDN
- Custom domains
- SSL certificates

### ✅ Railway (Backend)
- Free tier for Python apps
- Easy database setup
- Automatic HTTPS
- Simple deployment

---

## 🚀 STEP 1: DEPLOY BACKEND ON RAILWAY

### 1. Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub/GitLab
3. Get $5 free credit

### 2. Prepare Backend Repository
```bash
# Your backend is already ready with:
# - railway.toml configuration
# - health check endpoint
# - requirements.txt
```

### 3. Deploy to Railway
1. Click "New Project" → "Deploy from GitHub repo"
2. Select your repository
3. Railway will automatically detect it's a Python app
4. Add environment variables:
   ```
   DATABASE_URL=postgresql://postgres:password@localhost:5432/railway
   SECRET_KEY=your-secret-key-here
   ```
5. Click "Deploy"

### 4. Get Your Backend URL
After deployment, Railway will give you a URL like:
```
https://your-app-name.up.railway.app
```

---

## 🚀 STEP 2: DEPLOY FRONTEND ON VERCEL

### 1. Create Vercel Account
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Get free hobby plan

### 2. Prepare Frontend
Your frontend is already configured with:
- `vercel.json` configuration file
- Environment variable support

### 3. Deploy to Vercel
1. Click "New Project" → "Import Git Repository"
2. Select your repository
3. Vercel will detect it's a React app
4. Configure environment variables:
   ```
   VITE_API_BASE_URL=https://your-backend-url.up.railway.app/api
   ```
5. Click "Deploy"

### 4. Get Your Frontend URL
Vercel will give you a URL like:
```
https://your-app-name.vercel.app
```

---

## 🔧 CONFIGURATION DETAILS

### Backend Environment Variables (Railway)
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/railway
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend Environment Variables (Vercel)
```env
VITE_API_BASE_URL=https://your-backend-url.up.railway.app/api
```

---

## 🌐 ACCESS YOUR APPLICATION

After both deployments:

### 🎯 Your Live Application
- **Frontend**: `https://your-app-name.vercel.app`
- **Backend API**: `https://your-backend-url.up.railway.app/api`
- **API Docs**: `https://your-backend-url.up.railway.app/docs`

### 🔑 Default Login
```
Username: admin
Password: admin123
```

---

## 🔄 UPDATING YOUR APPLICATION

### Automatic Updates
Both Vercel and Railway support automatic deployments:
1. Push changes to your GitHub repository
2. Both platforms will automatically rebuild and deploy
3. Your application updates with zero downtime

### Manual Updates
- **Vercel**: Go to dashboard → View deployments → Redeploy
- **Railway**: Go to dashboard → Settings → Redeploy

---

## 🛠️ TROUBLESHOOTING

### Common Issues

#### CORS Errors
Add your Vercel domain to Railway CORS settings:
```python
# In backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-app-name.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### API Connection Issues
1. Check environment variables
2. Verify backend URL is correct
3. Check Railway logs for errors

#### Build Failures
1. Check `vercel.json` syntax
2. Verify `package.json` scripts
3. Check Railway logs for Python errors

---

## 💰 COST BREAKDOWN

### Free Tier Limits
- **Vercel**: 100GB bandwidth, unlimited projects
- **Railway**: $5 credit (enough for months of usage)
- **Database**: PostgreSQL included in Railway

### When to Upgrade
- **Vercel**: When you exceed 100GB bandwidth/month
- **Railway**: When $5 credit runs out (about 3-6 months)

---

## 🎯 NEXT STEPS

### 1. Custom Domain (Optional)
```bash
# On Vercel: Add custom domain
# On Railway: Add custom domain
```

### 2. Database Backups
Railway automatically backs up your database

### 3. Monitoring
Both platforms provide built-in monitoring and logs

---

## 🎉 SUCCESS!

Your Textile AI Management System is now live on:
- **Frontend**: Vercel (Fast, global CDN)
- **Backend**: Railway (Reliable Python hosting)

Both platforms automatically handle:
- ✅ SSL certificates
- ✅ Global CDN
- ✅ Automatic deployments
- ✅ Scaling
- ✅ Monitoring

**Your application is now production-ready!** 🚀
