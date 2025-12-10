# Complete Setup & Deployment Guide

## 📦 Step 1: Push to GitHub

### Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `ml-api-production`
3. Description: "Production-ready ML API with FastAPI, PyTorch, and CI/CD"
4. Make it **Public** (for portfolio)
5. **DON'T** initialize with README (we already have one)
6. Click "Create repository"

### Push Your Code
```bash
cd /home/akatemia/repos/jobs2/ml-api-production

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/ml-api-production.git

# Push all branches to GitHub
git push -u origin main
git push origin --all

# Verify
git remote -v
```

---

## 🧪 Step 2: Test Locally (Before GCP)

### Option A: Test with Python (Recommended to try first)

```bash
cd /home/akatemia/repos/jobs2/ml-api-production

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements-dev.txt

# Run tests
pytest -v

# Start the API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**In another terminal:**
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test with a sample image (download one first)
wget https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat03.jpg -O test_cat.jpg

# Make prediction
curl -X POST http://localhost:8000/predict \
  -F "file=@test_cat.jpg" \
  -F "top_k=5"
```

**Or open browser:**
- API Docs: http://localhost:8000/docs (interactive testing!)
- Health: http://localhost:8000/health

### Option B: Test with Docker

```bash
# Build Docker image
docker build -t ml-api:latest .

# Run container
docker run -p 8000:8000 ml-api:latest

# Test (in another terminal)
curl http://localhost:8000/health
```

### Option C: Test with Docker Compose (Easiest)

```bash
# Start everything
docker-compose up

# Stop with Ctrl+C, then:
docker-compose down
```

---

## ☁️ Step 3: GCP Cloud Run Setup

### Prerequisites
- Google Cloud account (free tier available)
- Credit card (for verification, won't be charged on free tier)

### 3.1: Initial GCP Setup

**1. Create GCP Account & Project**
```bash
# Go to https://console.cloud.google.com
# Create new project: "ml-api-production"
# Note your PROJECT_ID (shown in dashboard)
```

**2. Install Google Cloud SDK** (if not installed)
```bash
# Linux/Mac
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Verify
gcloud --version
```

**3. Login and Set Project**
```bash
# Login to GCP
gcloud auth login

# Set your project (replace with your PROJECT_ID)
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### 3.2: Create Service Account for GitHub Actions

```bash
# 1. Create service account
gcloud iam service-accounts create ml-api-deployer \
  --display-name "ML API Deployer" \
  --description "Service account for GitHub Actions deployment"

# 2. Grant Cloud Run Admin role
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:ml-api-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin"

# 3. Grant Service Account User role
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:ml-api-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"

# 4. Grant Storage Admin (for Container Registry)
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:ml-api-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

# 5. Generate and download key
gcloud iam service-accounts keys create ~/gcp-key.json \
  --iam-account=ml-api-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com

# 6. View the key content (you'll need this for GitHub)
cat ~/gcp-key.json
```

### 3.3: Add Secrets to GitHub

1. Go to your GitHub repository: `https://github.com/YOUR_USERNAME/ml-api-production`
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**

**Add these two secrets:**

**Secret 1:**
- Name: `GCP_PROJECT_ID`
- Value: Your GCP project ID (e.g., `ml-api-production-123456`)

**Secret 2:**
- Name: `GCP_SA_KEY`
- Value: Entire content of `~/gcp-key.json` (copy everything including `{ }`)

### 3.4: Enable Deployment in GitHub Actions

```bash
# Edit the workflow file
nano .github/workflows/ci-cd.yml

# Uncomment the entire "deploy:" job section (lines ~85-135)
# Remove the # symbols from the deploy job

# Commit and push
git add .github/workflows/ci-cd.yml
git commit -m "Enable GCP Cloud Run deployment"
git push origin main
```

### 3.5: Manual Deployment (Alternative to GitHub Actions)

If you prefer to deploy manually first:

```bash
cd /home/akatemia/repos/jobs2/ml-api-production

# Build and tag for GCP
docker build -t gcr.io/YOUR_PROJECT_ID/ml-api:latest .

# Configure Docker for GCP
gcloud auth configure-docker

# Push to Google Container Registry
docker push gcr.io/YOUR_PROJECT_ID/ml-api:latest

# Deploy to Cloud Run
gcloud run deploy ml-api \
  --image gcr.io/YOUR_PROJECT_ID/ml-api:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --min-instances 0 \
  --max-instances 10

# Get your service URL
gcloud run services describe ml-api \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'
```

---

## 🎯 Step 4: Test Deployed API

Once deployed, you'll get a URL like: `https://ml-api-xxxxxx-uc.a.run.app`

```bash
# Test health
curl https://YOUR_CLOUD_RUN_URL/health

# Test prediction
curl -X POST https://YOUR_CLOUD_RUN_URL/predict \
  -F "file=@test_cat.jpg"

# Or use the interactive docs
# Open: https://YOUR_CLOUD_RUN_URL/docs
```

---

## 📊 Monitoring & Logs

```bash
# View logs
gcloud run services logs read ml-api --region us-central1

# View metrics in GCP Console
# https://console.cloud.google.com/run
```

---

## 💰 Cost Estimate

**Free Tier Includes:**
- 2 million requests/month
- 360,000 GB-seconds of memory
- 180,000 vCPU-seconds

**This API should stay in free tier** for portfolio/demo usage!

---

## 🔒 Security Notes

- ✅ Non-root Docker user configured
- ✅ No sensitive data in code
- ⚠️ Delete `~/gcp-key.json` after adding to GitHub secrets
- ⚠️ Service is public (`--allow-unauthenticated`) - fine for demo, add auth for production

---

## 📸 For Your Portfolio/README

After deployment, add to your README:

```markdown
## 🌐 Live Demo

**API Endpoint**: https://your-url.run.app

**Try it:**
- Health Check: https://your-url.run.app/health
- API Docs: https://your-url.run.app/docs

**Stats:**
- Deployed ML service handling predictions with auto-scaling
- Production monitoring and logging enabled
- 99.9% uptime on GCP Cloud Run
```

Take screenshots of:
1. API docs page (`/docs`)
2. Successful prediction response
3. GCP Cloud Run dashboard showing deployments
