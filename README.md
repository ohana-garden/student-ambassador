# Student Ambassador

AI-powered college application and financial aid assistant.

## Quick Start

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## Development

Open in GitHub Codespaces for a pre-configured environment.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new)

## API

- `GET /` - Health check
- `POST /students` - Create student
- `GET /students/{id}` - Get student
- `POST /scholarships` - Create scholarship
- `GET /scholarships` - List scholarships
- `POST /students/{id}/matches` - Get scholarship matches
