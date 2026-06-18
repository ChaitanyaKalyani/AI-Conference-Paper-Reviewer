# 🚀 Deployment Guide

Complete guide for deploying the AI Conference Paper Reviewer application.

## Table of Contents
1. [Local Development](#local-development)
2. [Streamlit Cloud](#streamlit-cloud)
3. [Docker Deployment](#docker-deployment)
4. [Environment Configuration](#environment-configuration)
5. [Performance Optimization](#performance-optimization)
6. [Monitoring & Maintenance](#monitoring--maintenance)

## Local Development

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment support

### Setup Steps

```bash
# 1. Clone repository
git clone https://github.com/yourusername/Conference-Paper-Reviewer.git
cd Conference-Paper-Reviewer

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Upgrade pip
pip install --upgrade pip

# 4. Install dependencies
pip install -r requirements.txt

# 5. Download spaCy model
python -m spacy download en_core_web_sm

# 6. Configure environment
cp .env.example .env
# Edit .env with your OpenRouter API key

# 7. Run application
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Streamlit Cloud

### Pre-deployment Checklist
- ✅ Code committed to GitHub repository
- ✅ All sensitive data in `.env` (not hardcoded)
- ✅ `.gitignore` prevents credential commits
- ✅ `requirements.txt` updated with all dependencies
- ✅ README.md provides setup instructions

### Deployment Steps

1. **Push to GitHub**
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

2. **Connect to Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Click "New app"
   - Select your GitHub repository, branch, and main file (`app.py`)

3. **Add Secrets**
   - In Streamlit Cloud dashboard, go to "Settings" → "Secrets"
   - Add your secrets:
   ```
   OPENROUTER_API_KEY = "your_api_key_here"
   ```

4. **Deploy**
   - Click "Deploy"
   - Wait for build to complete (~2-3 minutes)

### Streamlit Configuration

Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#6495ff"
backgroundColor = "#0a0e27"
secondaryBackgroundColor = "#111827"
textColor = "#ffffff"
font = "sans serif"

[client]
showErrorDetails = true
toolbarMode = "viewer"

[logger]
level = "info"

[server]
port = 8501
headless = true
maxUploadSize = 200
```

## Docker Deployment

### Prerequisites
- Docker installed and running
- Docker Hub account (for image hosting)

### Dockerfile

Create `Dockerfile` in project root:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run

```bash
# Build image
docker build -t paper-reviewer:latest .

# Run container
docker run -p 8501:8501 \
  -e OPENROUTER_API_KEY=your_api_key \
  paper-reviewer:latest

# With Docker Compose
docker-compose up
```

### Docker Compose Configuration

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  paper-reviewer:
    build: .
    ports:
      - "8501:8501"
    environment:
      OPENROUTER_API_KEY: ${OPENROUTER_API_KEY}
      STREAMLIT_SERVER_PORT: 8501
      STREAMLIT_SERVER_ADDRESS: 0.0.0.0
    volumes:
      - ./output:/app/output
    restart: unless-stopped
```

## Environment Configuration

### Development (.env)
```env
OPENROUTER_API_KEY=your-openrouter-api-key
LLM_MODEL=openai/gpt-oss-20b:free
LLM_TEMPERATURE=0
LLM_TOP_P=0.1
MAX_PDF_PAGES=100
MAX_TEXT_LENGTH=50000
MAX_RETRIES=3
TIMEOUT_SECONDS=30
LOG_LEVEL=debug
```

### Production (.env)
```env
OPENROUTER_API_KEY=your-openrouter-api-key
LLM_MODEL=openai/gpt-4-turbo-preview
LLM_TEMPERATURE=0
LLM_TOP_P=0.1
MAX_PDF_PAGES=100
MAX_TEXT_LENGTH=50000
MAX_RETRIES=5
TIMEOUT_SECONDS=60
LOG_LEVEL=warning
```

## Performance Optimization

### Caching Strategies

1. **Model Caching**: Models loaded once and cached globally
   - SentenceTransformer loaded once per session
   - spaCy model loaded once per session
   - FAISS index cached in memory

2. **PDF Processing**: Limit page extraction
   ```python
   MAX_PDF_PAGES = 100  # Limit extraction to first 100 pages
   MAX_TEXT_LENGTH = 50000  # Truncate text to 50K chars
   ```

3. **API Rate Limiting**: Built-in retry with exponential backoff
   ```python
   MAX_RETRIES = 3  # Retry up to 3 times
   TIMEOUT_SECONDS = 30  # 30 second timeout
   ```

### Resource Optimization

- **Memory**: 2-4GB recommended
- **CPU**: Multi-core beneficial for parallel processing
- **Disk**: 5GB for ML models and cache

### Scaling Considerations

1. **Single Server**: Streamlit Cloud (up to 3 concurrent users free)
2. **Small Team**: Docker with load balancer
3. **Enterprise**: Kubernetes deployment with multiple replicas

## Monitoring & Maintenance

### Logging

Logs available in:
- Streamlit Cloud: Dashboard logs
- Docker: `docker logs <container_id>`
- Local: Console output or `logs/` directory

### Health Checks

Monitor API availability:
```bash
curl http://localhost:8501/_stcore/health
```

### Updates

Updating dependencies:
```bash
# Check for updates
pip list --outdated

# Update dependencies
pip install --upgrade -r requirements.txt
```

### Backup

Important files to backup:
- `.env` (API keys)
- `output/` (generated reports)
- `dataset/` (local paper datasets)

## Troubleshooting

### Issue: "Module not found" Error
```bash
# Solution: Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Issue: API Key Errors
```bash
# Verify API key in .env
cat .env | grep OPENROUTER_API_KEY

# Test API connection
python -c "from config import OPENROUTER_API_KEY; print('✅ Key loaded')"
```

### Issue: Slow Performance
```bash
# Check available resources
free -h  # Linux
vm_stat  # macOS
Get-ComputerInfo  # Windows

# Increase available memory/resources
```

### Issue: Port Already in Use
```bash
# Change port in config
streamlit run app.py --server.port 8502
```

## Security Checklist

- ✅ API keys in environment variables (not hardcoded)
- ✅ HTTPS enabled for production (Streamlit Cloud/Docker reverse proxy)
- ✅ Input validation for all user inputs
- ✅ CORS configured appropriately
- ✅ Rate limiting implemented
- ✅ Regular dependency updates
- ✅ No sensitive data in logs

## Contact & Support

For deployment issues:
1. Check Streamlit documentation: https://docs.streamlit.io
2. Review Docker documentation: https://docs.docker.com
3. Check troubleshooting section above
4. Open an issue on GitHub

---

**Last Updated**: January 2025
**Tested With**: Python 3.10, Streamlit 1.58.0, Docker 24.0
