# ML Image Classification API

[![CI/CD Pipeline](https://github.com/yourusername/ml-api-production/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/yourusername/ml-api-production/actions)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.1.0-EE4C2C.svg)](https://pytorch.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-ready Machine Learning API for image classification built with **FastAPI** and **PyTorch**. This service uses a pre-trained ResNet-18 model to classify images into 1000 ImageNet categories with confidence scores.

## 🚀 Features

- **Fast & Modern**: Built with FastAPI for high performance and automatic OpenAPI documentation
- **Production-Ready ML**: Pre-trained ResNet-18 model for accurate image classification
- **Containerized**: Multi-stage Docker builds for optimized deployment
- **CI/CD Pipeline**: Automated testing and deployment with GitHub Actions
- **Comprehensive Testing**: Full test suite with pytest and coverage reporting
- **Structured Logging**: JSON-formatted logs for production monitoring
- **Health Checks**: Built-in endpoint for service monitoring
- **Auto-scaling Ready**: Designed for deployment on GCP Cloud Run

## 🛠️ Tech Stack

- **Python 3.11** - Latest stable Python version
- **FastAPI** - Modern, fast web framework for building APIs
- **PyTorch** - Deep learning framework with pre-trained ResNet-18
- **Uvicorn** - ASGI server for production deployment
- **Docker** - Containerization with multi-stage builds
- **GitHub Actions** - Automated CI/CD pipeline
- **pytest** - Comprehensive testing framework

## 📁 Project Structure

```
ml-api-production/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models/
│   │   ├── __init__.py
│   │   └── classifier.py    # ResNet-18 model wrapper
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py        # API endpoints
│   │   └── schemas.py       # Pydantic models
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Configuration management
│   │   └── logging.py       # Logging setup
│   └── utils/
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── test_api.py          # API endpoint tests
│   └── test_model.py        # Model tests
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # CI/CD pipeline
├── Dockerfile               # Multi-stage production build
├── docker-compose.yml       # Local development setup
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── pytest.ini               # Test configuration
├── .dockerignore
├── .gitignore
└── README.md
```

## 🚦 Quick Start

### Local Development (Python)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ml-api-production.git
   cd ml-api-production
   ```

2. **Create virtual environment**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Run the API**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the API**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

### Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build -t ml-api:latest .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 ml-api:latest
   ```

### Docker Compose (Recommended for Development)

```bash
docker-compose up
```

## 📖 API Documentation

### Health Check

**GET** `/health`

Check the health status of the API.

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "model_loaded": true
}
```

### Image Classification

**POST** `/predict`

Upload an image to get classification predictions.

**Parameters:**
- `file`: Image file (JPEG, PNG, etc.)
- `top_k`: Number of top predictions to return (default: 5, max: 10)

**Example using cURL:**
```bash
curl -X POST http://localhost:8000/predict \
  -F "file=@path/to/your/image.jpg" \
  -F "top_k=5"
```

**Example using Python:**
```python
import requests

url = "http://localhost:8000/predict"
files = {"file": open("image.jpg", "rb")}
params = {"top_k": 5}

response = requests.post(url, files=files, params=params)
print(response.json())
```

**Response:**
```json
{
  "success": true,
  "predictions": [
    {"class_name": "golden_retriever", "confidence": 0.87},
    {"class_name": "labrador", "confidence": 0.08},
    {"class_name": "dog", "confidence": 0.03},
    {"class_name": "puppy", "confidence": 0.01},
    {"class_name": "animal", "confidence": 0.01}
  ],
  "message": "Successfully classified image.jpg"
}
```

## 🧪 Testing

Run the full test suite with coverage:

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests with coverage
pytest --cov=app --cov-report=term-missing -v

# Run specific test files
pytest tests/test_api.py -v
pytest tests/test_model.py -v
```

## 🔧 Configuration

Configuration is managed through environment variables. Create a `.env` file:

```env
# API Settings
API_TITLE=ML Image Classification API
API_VERSION=0.1.0
DEBUG=false

# Server Settings
HOST=0.0.0.0
PORT=8000

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Model Settings
MODEL_NAME=resnet18
MODEL_DEVICE=cpu  # or 'cuda' for GPU
```

## 🚀 CI/CD Pipeline

The project includes a complete GitHub Actions workflow that:

1. **Tests**: Runs pytest with coverage on every push/PR
2. **Linting**: Checks code quality with flake8
3. **Docker Build**: Builds and tests the Docker image
4. **Deployment**: Ready for deployment to GCP Cloud Run (see deployment section)

## ☁️ Deployment to GCP Cloud Run

### Prerequisites
1. Google Cloud Platform account
2. GCP project with Cloud Run and Container Registry enabled
3. Service account with necessary permissions

### Setup Instructions

1. **Create GCP Service Account**
   ```bash
   gcloud iam service-accounts create ml-api-deployer \
     --display-name "ML API Deployer"
   ```

2. **Grant necessary permissions**
   ```bash
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
     --member="serviceAccount:ml-api-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
     --role="roles/run.admin"
   ```

3. **Generate and download key**
   ```bash
   gcloud iam service-accounts keys create key.json \
     --iam-account=ml-api-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com
   ```

4. **Add GitHub Secrets**
   - `GCP_SA_KEY`: Content of key.json file
   - `GCP_PROJECT_ID`: Your GCP project ID

5. **Uncomment deployment job** in `.github/workflows/ci-cd.yml`

6. **Push to main branch** to trigger automatic deployment

### Manual Deployment

```bash
# Build and tag image
docker build -t gcr.io/YOUR_PROJECT_ID/ml-api:latest .

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
```

## 📊 Performance & Monitoring

- **Auto-scaling**: Automatically scales based on traffic (0-10 instances)
- **Health Checks**: Built-in health endpoint for monitoring
- **Structured Logging**: JSON logs for easy parsing and analysis
- **Request Tracking**: All requests logged with predictions

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Pre-trained ResNet-18 model from [PyTorch Model Zoo](https://pytorch.org/vision/stable/models.html)
- FastAPI framework by [Sebastián Ramírez](https://github.com/tiangolo)
- ImageNet dataset for model training

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Built with ❤️ for production ML deployments**
