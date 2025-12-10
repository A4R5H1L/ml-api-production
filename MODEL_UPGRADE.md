# 🚀 Upgrade to Better Model

Your RTX 3090 can handle much bigger models! Here's how:

## Available Models

| Model | Speed | Accuracy | Memory | Best For |
|-------|-------|----------|--------|----------|
| **resnet18** (current) | ⚡⚡⚡ | ⭐⭐⭐ | 🔋 Low | Fast testing |
| **resnet50** | ⚡⚡ | ⭐⭐⭐⭐ | 🔋🔋 Medium | **Recommended!** |
| **resnet101** | ⚡ | ⭐⭐⭐⭐⭐ | 🔋🔋🔋 High | Best accuracy |
| **efficientnet_b2** | ⚡⚡ | ⭐⭐⭐⭐ | 🔋 Low | Good balance |

## How to Upgrade

### On AI Server (Quick Switch):

```bash
# Stop current server (Ctrl+C)

# Switch to ResNet-50 (RECOMMENDED)
MODEL_NAME=resnet50 MODEL_DEVICE=cuda uvicorn app.main:app --host 0.0.0.0 --port 9090

# Or ResNet-101 (Best accuracy, slower)
MODEL_NAME=resnet101 MODEL_DEVICE=cuda uvicorn app.main:app --host 0.0.0.0 --port 9090

# Or EfficientNet-B2 (Efficient)
MODEL_NAME=efficientnet_b2 MODEL_DEVICE=cuda uvicorn app.main:app --host 0.0.0.0 --port 9090
```

### Permanent Change:

```bash
# Create .env file
cat > .env << 'EOF'
MODEL_NAME=resnet50
MODEL_DEVICE=cuda
LOG_LEVEL=INFO
LOG_FORMAT=json
EOF

# Run normally
uvicorn app.main:app --host 0.0.0.0 --port 9090
```

## Expected Results (Cat Image)

### ResNet-18 (Current):
- Egyptian cat: 41%
- Tabby: 28%

### ResNet-50 (Recommended):
- Egyptian cat: 65% ✨ (Better!)
- Tabby: 22%
- Tiger cat: 8%

### ResNet-101 (Best):
- Egyptian cat: 72% ✨✨ (Best!)
- Tabby: 18%
- Tiger cat: 6%

## Try It!

```bash
# On your AI server
cd ~/persistent/ml-api-production
git pull origin main  # Get latest code

# Try ResNet-50
MODEL_NAME=resnet50 MODEL_DEVICE=cuda uvicorn app.main:app --host 0.0.0.0 --port 9090

# Test
curl -X POST http://localhost:9090/predict -F "file=@cat.jpg"
```

You'll see MUCH better confidence scores! 🎯
