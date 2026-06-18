# 🎓 AI Conference Paper Reviewer

An intelligent AI-powered system for automated conference paper review and analysis. This application leverages advanced NLP, machine learning, and RAG (Retrieval-Augmented Generation) to provide comprehensive peer-review analysis.

## ✨ Features

### Core Analysis
- **📄 PDF Processing**: Extract and analyze research papers in PDF format
- **📝 Intelligent Summarization**: Generate executive summaries of research papers
- **⚖️ Peer Review Generation**: Automatically generate IEEE-style conference reviews with scoring
- **🎯 Problem Extraction**: Identify and extract research problem statements
- **💡 Contribution Analysis**: Automatically extract research contributions
- **📊 Named Entity Extraction**: Extract key entities and technical concepts

### Scoring System
- **Novelty Score** (0-10): Innovation and originality of the research
- **Technical Quality Score** (0-10): Rigor and technical soundness
- **Clarity Score** (0-10): Presentation and clarity of writing
- **Significance Score** (0-10): Impact and relevance of findings
- **Overall Recommendation**: Accept/Minor Revision/Major Revision/Reject

### Advanced Features
- **🔍 Domain Classification**: Automatic research domain identification (NLP, CV, ML, Security, Data Mining)
- **📚 Similar Papers Search**: Find related papers from arXiv
- **📊 Analytics Dashboard**: Comprehensive statistics and visualizations
- **📥 Multi-format Export**: Download reviews as PDF or text reports
- **🔗 RAG Integration**: Retrieve relevant papers for contextual analysis

## 🚀 Quick Start

### Installation

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/Conference-Paper-Reviewer.git
cd Conference-Paper-Reviewer
```

2. **Create Virtual Environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment**
```bash
cp .env.example .env
# Edit .env and add your OpenRouter API key
# Get API key from: https://openrouter.ai
```

5. **Download spaCy Model**
```bash
python -m spacy download en_core_web_sm
```

### Running the Application

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 📋 Requirements

### System Requirements
- Python 3.8+
- 4GB RAM minimum (8GB recommended for optimal performance)
- Internet connection for API calls and arXiv search

### API Requirements
- **OpenRouter API Key** (free tier available)
  - Sign up: https://openrouter.ai
  - Get your API key from the dashboard

## 🏗️ Architecture

### Core Modules

| Module | Purpose |
|--------|---------|
| `llm_utils.py` | Centralized LLM client, retry logic, error handling |
| `reviewer.py` | IEEE-style review generation with scoring |
| `summarizer.py` | Executive paper summarization |
| `problem_extractor.py` | Research problem statement extraction |
| `contribution_extractor.py` | Research contribution extraction |
| `score_parser.py` | Extract numerical scores from reviews |
| `report_generator.py` | Professional PDF/text report generation |
| `domain_classifier.py` | Research domain classification |
| `entity_extractor.py` | Named entity recognition (spaCy) |
| `arxiv_retriever.py` | arXiv paper search and retrieval |
| `rag_engine.py` | FAISS-based RAG engine |
| `rag_ranker.py` | Semantic similarity ranking |
| `recommendation_parser.py` | Extract recommendation from review |

## 🎯 Usage Guide

### Basic Workflow

1. **Upload Paper**: Click "Upload PDF" to select your research paper
2. **View Summary**: See the AI-generated paper summary
3. **Generate Review**: Click "Generate Review" to create a peer review
4. **View Analysis**: Check scores, recommendation, and detailed review
5. **Export Report**: Download review as PDF or text format

### Tab Navigation

- **📊 Summary Tab**: Paper overview, key contributions, domain classification
- **📝 Review Tab**: Detailed peer review, scores, recommendation
- **📈 Analytics Tab**: Statistics, related papers, domain trends

## 🔧 Configuration

### Environment Variables (.env)

```env
# API Configuration
OPENROUTER_API_KEY=your_api_key_here
LLM_MODEL=openai/gpt-oss-20b:free

# LLM Settings
LLM_TEMPERATURE=0
LLM_TOP_P=0.1

# Application Limits
MAX_PDF_PAGES=100
MAX_TEXT_LENGTH=50000
MAX_RETRIES=3
TIMEOUT_SECONDS=30
LOG_LEVEL=info
```

## 📊 Scoring Methodology

### Score Calculation
- Each dimension (Novelty, Technical Quality, Clarity, Significance) is scored 0-10
- Overall Score = Average of the four dimensions
- Final Recommendation based on overall score and qualitative analysis

### Recommendation Scale
- **Accept**: Overall Score ≥ 8.0
- **Minor Revision**: Overall Score 6.0-7.9
- **Major Revision**: Overall Score 4.0-5.9
- **Reject**: Overall Score < 4.0

## 🔐 Security

- ✅ **API Key Protection**: Secrets managed via environment variables (never hardcoded)
- ✅ **Input Validation**: All user inputs sanitized and validated
- ✅ **Error Handling**: Comprehensive error handling with retry logic
- ✅ **Rate Limiting**: Built-in throttling to prevent API overuse
- ✅ **.gitignore**: Prevents accidental credential commits

## 📈 Performance

- **Startup Time**: ~2-3 seconds (first run may take longer for model loading)
- **Paper Processing**: 30-60 seconds per paper (depending on size and API response)
- **Memory Usage**: 2-4GB during operation
- **Concurrent Users**: Single-user local instance (multi-user via deployment)

## 🐳 Deployment

### Streamlit Cloud Deployment

1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Add secrets via Streamlit dashboard:
   - OPENROUTER_API_KEY
4. Deploy with one click

### Docker Deployment

```bash
docker build -t paper-reviewer .
docker run -p 8501:8501 -e OPENROUTER_API_KEY=your_key paper-reviewer
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 📚 Documentation

- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- [API_DOCS.md](API_DOCS.md) - Module API documentation
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines

## 🐛 Troubleshooting

### Common Issues

**"API Key not found" Error**
- Ensure `.env` file exists and contains `OPENROUTER_API_KEY`
- Verify API key is valid at https://openrouter.ai

**PDF Upload Fails**
- Check file size (max 200MB)
- Ensure PDF is not corrupted
- Try with sample PDF first

**Slow Performance**
- First run loads ML models (expected delay)
- Subsequent runs are faster
- Increase available RAM if persistent

**Import Errors**
- Run `pip install -r requirements.txt` again
- Ensure Python 3.8+ is installed
- Try in a fresh virtual environment

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- LLM powered by [OpenRouter](https://openrouter.ai)
- NLP models from [spaCy](https://spacy.io) and [Sentence-Transformers](https://huggingface.co/sentence-transformers)
- Similarity search via [FAISS](https://github.com/facebookresearch/faiss)

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review troubleshooting section

---

**Made with ❤️ for the research community**
