# 🚀 Quick Start Guide

## I Can't Push to GitHub For You Because...
- Requires your GitHub username/password or SSH key
- Need to create the repository on GitHub first

## Here's What YOU Need to Do:

### 1️⃣ Push to GitHub (5 minutes)

```bash
# Go to https://github.com/new and create repository "ml-api-production"
# Then run:

cd /home/akatemia/repos/jobs2/ml-api-production
git remote add origin https://github.com/YOUR_USERNAME/ml-api-production.git
git push -u origin main
git push origin --all  # Push all feature branches too
```

### 2️⃣ Test Locally RIGHT NOW (easiest option)

```bash
cd /home/akatemia/repos/jobs2/ml-api-production

# Option A: Python venv (if installed)
python3.11 -m venv venv 2>/dev/null || python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Then open browser:** http://localhost:8000/docs

```bash
# Option B: Docker (easier, no Python setup needed)
docker-compose up
```

**Then open browser:** http://localhost:8000/docs

### 3️⃣ GCP Cloud Run Setup (optional, for portfolio)

**What you need:**
1. Google Cloud account (free tier: https://cloud.google.com/free)
2. Install gcloud CLI: https://cloud.google.com/sdk/docs/install

**Quick deploy:**
```bash
# Login
gcloud auth login

# Create project (or use existing)
gcloud projects create ml-api-prod-123 --name="ML API"
gcloud config set project ml-api-prod-123

# Enable APIs
gcloud services enable run.googleapis.com containerregistry.googleapis.com

# Deploy (will prompt for region, choose closest to you)
gcloud run deploy ml-api \
  --source . \
  --platform managed \
  --allow-unauthenticated \
  --memory 2Gi
```

**That's it!** You'll get a URL like `https://ml-api-xxx.run.app`

### 4️⃣ For GitHub Actions Auto-Deploy

See full `SETUP_GUIDE.md` for:
- Creating service account
- Adding GitHub secrets
- Enabling the deployment job

---

## 🎯 TL;DR - Test It Now!

**Fastest way to see it work:**

```bash
cd /home/akatemia/repos/jobs2/ml-api-production
docker-compose up
```

Open: http://localhost:8000/docs

Click "POST /predict" → "Try it out" → Upload an image → "Execute"

---

## ❓ What Each File Does

- `app/main.py` - FastAPI app entry point
- `app/models/classifier.py` - ResNet-18 ML model
- `app/api/routes.py` - API endpoints (/health, /predict)
- `Dockerfile` - Production container build
- `docker-compose.yml` - Local dev environment
- `.github/workflows/ci-cd.yml` - Auto-test & deploy
- `tests/` - Pytest test suite

---

## 📸 For Your Resume/Portfolio

After deploying, add to README:
```
🌐 Live Demo: https://your-url.run.app
📊 Handling ML predictions with auto-scaling on GCP Cloud Run
✅ Production monitoring and CI/CD pipeline
```
