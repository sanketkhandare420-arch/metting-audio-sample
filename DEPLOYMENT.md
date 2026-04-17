# Deployment Guide - Audio Action-Item Extractor

## Quick Deployment Comparison

| Platform | Setup Time | Cost | Ease | Best For |
|----------|-----------|------|------|----------|
| **Railway.app** | 5 min | Free tier | ⭐⭐⭐⭐⭐ | Most users |
| **PythonAnywhere** | 10 min | Free tier | ⭐⭐⭐⭐⭐ | Beginners |
| **Docker + DigitalOcean** | 30 min | $5/mo | ⭐⭐⭐⭐ | Scalability |
| **Windows Server** | 15 min | On-premise | ⭐⭐⭐ | Internal use |

---

## 🚀 Recommended: Railway.app (5 minutes)

### Step 1: Prepare Repository
```bash
# Initialize git repo if not already done
git init
git add .
git commit -m "Initial commit"
git branch -M main
```

### Step 2: Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/meeting-audio-analyzer.git
git push -u origin main
```

### Step 3: Deploy on Railway
1. Go to [railway.app](https://railway.app)
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Connect your GitHub account and select the repository
4. Railway auto-detects Flask and deploys
5. Your site is live at `https://meeting-audio-analyzer-xxx.up.railway.app`

### Step 4: Set Environment Variables (Optional)
In Railway dashboard:
- `FLASK_ENV` = `production`
- `SECRET_KEY` = (generate a random key)

---

## 🐳 Docker Deployment (More Control)

### Build & Run Locally
```bash
# Build image
docker build -t meeting-analyzer .

# Run locally
docker run -p 5000:5000 meeting-analyzer

# Visit http://localhost:5000
```

### Deploy to Cloud
- **Google Cloud Run** (serverless, pay-per-use)
- **DigitalOcean App Platform** (simpler, ~$12/mo)
- **AWS ECS** (enterprise)

---

## 🪟 Windows Server Deployment

### Prerequisites
- Python 3.10+ installed
- ffmpeg installed (`choco install ffmpeg`)

### Setup
```bash
# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Run production server
gunicorn --workers 4 --bind 0.0.0.0:5000 wsgi:app
```

### Keep Running (Task Scheduler)
1. Create batch file: `run_server.bat`
   ```batch
   cd C:\path\to\project
   python -m gunicorn --workers 4 --bind 0.0.0.0:5000 wsgi:app
   ```
2. Open Task Scheduler → Create task → Set to run on startup

### Access from Network
- Local machine: `http://localhost:5000`
- Other machines: `http://<YOUR_COMPUTER_IP>:5000`
  - Find IP: `ipconfig` → IPv4 Address

---

## Database Notes

- **SQLite** (current): Works fine for small deployments (<1000 users)
- **For scaling**: Upgrade to PostgreSQL
  ```python
  # Update DATABASE_URI
  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@host:5432/dbname'
  ```

---

## Security Checklist Before Deploying

- [ ] Change `app.secret_key` to a random string
- [ ] Set `FLASK_ENV=production`
- [ ] Disable debug mode
- [ ] Use HTTPS (all platforms provide this)
- [ ] Validate file uploads
- [ ] Set upload size limits
- [ ] Clean old files regularly

---

## Recommended Path for You

1. **Start**: Railway.app (free, instant)
2. **Scale**: Docker + DigitalOcean (more control)
3. **Enterprise**: AWS/Google Cloud (full features)

Any questions on deployment? Let me know!
