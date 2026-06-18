# 🤝 Contributing Guidelines

Thank you for your interest in contributing to the AI Conference Paper Reviewer! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the problem, not the person
- Help others learn and grow

## Getting Started

### Fork & Clone

```bash
# Fork the repository on GitHub
git clone https://github.com/yourusername/Conference-Paper-Reviewer.git
cd Conference-Paper-Reviewer
git remote add upstream https://github.com/original/Conference-Paper-Reviewer.git
```

### Set Up Development Environment

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies with dev tools
pip install -r requirements.txt
pip install black flake8 pytest  # Development tools

# Download spaCy model
python -m spacy download en_core_web_sm
```

### Configure Git

```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

## Development Workflow

### 1. Create a Branch

```bash
# Sync with upstream
git fetch upstream
git rebase upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
```

**Branch naming conventions**:
- `feature/` - New features
- `bugfix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions

### 2. Make Changes

Follow these guidelines:

**Code Style**:
```bash
# Format code with Black
black modules/ app.py

# Check with flake8
flake8 modules/ app.py
```

**Docstring Format**:
```python
def my_function(param1: str, param2: int) -> str:
    """
    Short description of function.
    
    Longer description providing more context about what
    the function does, its behavior, and any special cases.
    
    Args:
        param1 (str): Description of param1
        param2 (int): Description of param2
    
    Returns:
        str: Description of return value
    
    Raises:
        ValueError: When param1 is empty
        TypeError: When param2 is not an integer
    
    Example:
        >>> result = my_function("test", 42)
        >>> print(result)
        processed: test (42)
    """
    pass
```

**Type Hints**:
```python
from typing import List, Dict, Optional, Tuple

def process_papers(
    papers: List[Dict[str, str]],
    limit: Optional[int] = None
) -> Tuple[List[str], int]:
    """Process papers and return results."""
    pass
```

### 3. Test Your Changes

```bash
# Run existing tests
pytest tests/

# Add tests for new features
# Example test file: tests/test_llm_utils.py
```

**Testing Requirements**:
- Test coverage minimum: 70%
- All tests must pass
- Include edge cases
- Test error handling

### 4. Commit Changes

```bash
# Stage changes
git add .

# Commit with clear message
git commit -m "feat: add citation analysis module

- Extract and analyze paper citations
- Support for various citation formats
- Includes comprehensive tests

Fixes #123"
```

**Commit Message Format**:
```
<type>: <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting, missing semicolons)
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `test`: Test additions/updates

### 5. Push & Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name

# Open pull request on GitHub
# - Provide clear title and description
# - Reference related issues
# - Add screenshots for UI changes
```

**Pull Request Template**:
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Fixes #123

## Testing
Describe how you tested the changes:
- [ ] Tested locally
- [ ] All tests pass
- [ ] Added new tests

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes
```

## Code Review Process

### For Contributors

1. Address all feedback
2. Push follow-up commits
3. Request re-review
4. Be patient and respectful

### For Reviewers

1. Review promptly
2. Provide constructive feedback
3. Approve clear, quality contributions
4. Test changes locally if needed

## Types of Contributions

### Bug Reports

Use the bug report template:
```markdown
## Description
Clear description of the bug

## Steps to Reproduce
1. Step one
2. Step two
3. ...

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., macOS]
- Python: [e.g., 3.10]
- Version: [commit hash or version]

## Screenshots
If applicable
```

### Feature Requests

Use the feature request template:
```markdown
## Description
Clear description of the feature

## Problem Statement
What problem does this solve?

## Proposed Solution
How would you implement this?

## Alternatives Considered
Other approaches you considered

## Additional Context
Any additional information
```

### Documentation Improvements

- Fix typos and grammar
- Clarify confusing sections
- Add examples
- Update API documentation
- Add diagrams/images

## Development Areas

### High Priority
- Performance optimizations
- Additional LLM providers
- Advanced visualization features
- Multi-language support
- Batch processing

### Medium Priority
- User authentication
- Caching improvements
- Enhanced error messages
- More export formats
- API endpoint exposure

### Low Priority
- UI theme alternatives
- Additional metrics
- Extended logging options
- Analytics integrations

## Testing Guidelines

### Unit Tests
```python
# tests/test_modules.py
import pytest
from modules.reviewer import generate_review

def test_generate_review_basic():
    sections = {"abstract": "test"}
    review = generate_review(sections)
    assert "Novelty Score" in review
    assert isinstance(review, str)

def test_generate_review_empty():
    with pytest.raises(ValueError):
        generate_review({})
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=modules

# Run specific test
pytest tests/test_reviewer.py::test_generate_review_basic
```

## Documentation Standards

### README Sections
- Features
- Quick Start
- Installation
- Usage
- Configuration
- Troubleshooting
- Contributing
- License

### Code Documentation
- Module docstrings
- Function docstrings
- Inline comments for complex logic
- Type hints for all functions
- Example usage in docstrings

### Changelog
Update `CHANGELOG.md`:
```markdown
## [1.1.0] - 2025-01-20

### Added
- New citation analysis feature
- Batch processing support

### Fixed
- Memory leak in RAG engine
- Unicode handling in PDF generation

### Changed
- Improved error messages
- Updated dependencies
```

## Performance Guidelines

### Code Performance
- Avoid nested loops where possible
- Use lazy loading for large models
- Cache expensive computations
- Profile code before optimization

### Memory Usage
- Monitor model loading
- Clear unused variables
- Use generators for large datasets
- Profile memory with `memory_profiler`

## Security Guidelines

- Never commit API keys or secrets
- Use environment variables
- Validate all user inputs
- Sanitize output for safety
- Report security issues privately to maintainers

## Release Process

1. Update version in `__init__.py`
2. Update `CHANGELOG.md`
3. Update documentation
4. Create release notes
5. Tag release: `git tag v1.1.0`
6. Push tags: `git push origin --tags`

## Resources

### Documentation
- [Python Style Guide (PEP 8)](https://www.python.org/dev/peps/pep-0008/)
- [Google Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Streamlit Documentation](https://docs.streamlit.io)

### Tools
- [Black Formatter](https://black.readthedocs.io/)
- [Flake8 Linter](https://flake8.pycqa.org/)
- [Pytest Testing](https://docs.pytest.org/)

### Communities
- GitHub Issues
- Discussions
- Stack Overflow

## Support

### Getting Help
- Check existing issues and discussions
- Review documentation
- Ask in GitHub discussions
- Open an issue with details

### Reporting Issues
- Use issue templates
- Include minimal reproducible example
- Provide system information
- Check existing issues first

## Recognition

Contributors are recognized in:
- `CONTRIBUTORS.md`
- Release notes
- GitHub contributor list

Thank you for contributing! 🎉

---

**Last Updated**: January 2025
**Maintained By**: [Your Name/Organization]
