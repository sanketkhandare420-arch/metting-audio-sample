# Railway.app Deployment Guide

Railway.app is the fastest way to deploy your Flask app with zero configuration. It takes about **5 minutes**.

---

## ✅ Deployment Steps

### Step 1: Install Git and Initialize Repository

```bash
# Check if git is installed
git --version

# If not, download from https://git-scm.com

# Navigate to your project folder
cd "C:\Users\USER\Desktop\metting audio sample"

# Initialize git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Audio Action-Item Extractor"
```

**Expected output:**
```
[master (root-commit) abc1234] Initial commit
 X files changed, Y insertions(+)
```

---

### Step 2: Create GitHub Account and Repository

1. Go to [github.com](https://github.com) → Sign up (free)
2. Create new repository:
   - Name: `meeting-audio-analyzer`
   - Description: "AI-powered meeting transcription and action item extraction"
   - Public or Private (your choice)
   - **Do NOT** check "Initialize with README" (you already have one)
3. Click **"Create repository"**

You'll see instructions like:
```
git remote add origin https://github.com/YOUR_USERNAME/meeting-audio-analyzer.git
git branch -M main
git push -u origin main
```

---

### Step 3: Push Code to GitHub

Copy and run the commands from Step 2:

```bash
# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/meeting-audio-analyzer.git

# Rename branch to main
git branch -M main

# Push code
git push -u origin main
```

**Expected output:**
```
Enumerating objects: 50, done.
Counting objects: 100% (50/50), done.
...
* [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

✅ Your code is now on GitHub!

---

### Step 4: Deploy to Railway.app

1. Go to [railway.app](https://railway.app)
2. Click **"Start a New Project"**
3. Choose **"Deploy from GitHub repo"**
4. **Authenticate with GitHub**
   - Click "Install Railway on GitHub"
   - Select your repository
   - Click "Install"
5. Select `meeting-audio-analyzer` repository
6. Railway automatically detects it's Flask and starts deployment
7. **Wait 1-2 minutes** for deployment to complete

---

### Step 5: Access Your Deployed App

Once deployment completes:
- Railway shows you a live URL: `https://meeting-audio-analyzer-xxx.up.railway.app`
- Click the link → Your app is **live**! 🎉

---

## ⚙️ Configure Environment Variables

In Railway dashboard:

1. Go to your project → Settings tab
2. Scroll down to **Variables**
3. Add these variables:

| Variable | Value |
|----------|-------|
| `FLASK_ENV` | `production` |
| `SECRET_KEY` | (generate random: `python -c "import secrets; print(secrets.token_hex(16))"`) |

**Click "Deploy" button after each change**

---

## 🔧 Database Persistence

Railway's free plan has limitations. For better reliability:

### Option A: Keep SQLite (works fine for < 1000 users)
- Database is stored in Railway's ephemeral storage
- Data persists between deploys
- **Free**

### Option B: Use PostgreSQL (recommended for scale)
1. In Railway, click **"Add Service"** → **"PostgreSQL"**
2. Railway automatically creates a database and sets `DATABASE_URL`
3. Update `app.py`:
   ```python
   import os
   DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///meeting_history.db')
   app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
   ```
4. **Commit and push**:
   ```bash
   git add app.py
   git commit -m "Add PostgreSQL support"
   git push
   ```
5. Railway auto-redeploys

---

## 📤 Uploading Files (Handling Audio Uploads)

Railway gives you `/tmp` for temporary files. Update your app:

```python
import tempfile

# Instead of 'uploads/', use temp directory
UPLOAD_FOLDER = tempfile.gettempdir()

# Or use Railway's persistent storage for uploaded files:
# UPLOAD_FOLDER = os.getenv('UPLOAD_DIR', 'uploads')
```

---

## ✨ Advanced: Custom Domain

1. Go to Railway dashboard → Your project
2. Click **"Settings"** → **"Domains"**
3. Add your domain (e.g., `analyzer.mycompany.com`)
4. Update DNS at your domain registrar (Railway provides instructions)
5. SSL certificate auto-generated (HTTPS enabled)

---

## 🚨 Troubleshooting

### App crashes after deploy?
1. Check logs: Railway dashboard → **Logs** tab
2. Look for errors like:
   - `ModuleNotFoundError` → Missing package in `requirements.txt`
   - `ImportError` → Check `models.py` path

### Database errors?
```python
# Make sure SQLAlchemy handles startup errors:
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Database init error: {e}")
```

### Audio not processing?
- ffmpeg must be installed in Railway's container
- Update `Dockerfile` to include it (already done)

### Files not persisting?
- Use PostgreSQL instead of SQLite
- Or save to Cloud Storage (S3, Railway Volumes)

---

## 📊 Monitor Your Deployment

Railway dashboard shows:
- **Memory usage**
- **CPU usage**
- **Request logs**
- **Build logs**

If app slows down:
- Increase "Memory" allocation in Settings
- Upgrade from free tier ($5/month)

---

## 🎯 Summary

| Step | Time | Status |
|------|------|--------|
| 1. Initialize Git repo | 1 min | ✅ Done locally |
| 2. Create GitHub account | 2 min | Now |
| 3. Push to GitHub | 1 min | `git push` |
| 4. Deploy to Railway | 2 min | Click → Wait |
| 5. Access live app | 1 min | Open URL |

**Total: ~7 minutes from zero to production** 🚀

---

## Next Steps

After deployment:
- Test your live app with a meeting recording
- Share the URL with team members
- Monitor usage in Railway dashboard
- Set up auto-deploys (Railway does this by default)

Any issues? Check Railway logs or ask for help!
