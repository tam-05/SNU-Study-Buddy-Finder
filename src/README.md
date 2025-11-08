# Source Code Directory

This directory contains the main application source code.

## Files

- `api.py` - FastAPI REST API backend
- `streamlit_app.py` - Streamlit web application frontend

## API Backend (api.py)

RESTful API for study buddy recommendations.

### Features
- Student profile retrieval
- Buddy recommendations with filtering
- System statistics
- Health checks
- Pagination support

### Running
```bash
python src/api.py
```

Access at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Key Endpoints
- `GET /api/student/{id}` - Get student profile
- `POST /api/recommendations` - Get recommendations
- `GET /api/stats` - System statistics
- `GET /api/students` - List all students

## Web Application (streamlit_app.py)

Interactive web interface for finding study buddies.

### Features
- Student profile display
- Interactive recommendation filtering
- Real-time compatibility scoring
- Visualizations and analytics
- Modern UI with custom styling

### Running
```bash
streamlit run src/streamlit_app.py
```

Access at: http://localhost:8501

### UI Components
- **Sidebar**: Student selection and filters
- **Profile Card**: Current student information
- **Recommendations**: Matched study buddies
- **Analytics**: System statistics and insights

## Architecture

```
┌─────────────┐
│   User      │
└──────┬──────┘
       │
       ├─────────────┐
       │             │
┌──────▼──────┐ ┌───▼────────┐
│  Streamlit  │ │  FastAPI   │
│     App     │ │    API     │
└──────┬──────┘ └───┬────────┘
       │            │
       └────┬───────┘
            │
    ┌───────▼────────┐
    │  Model Layer   │
    │ (joblib files) │
    └────────────────┘
```

## Development

### Adding New Features

1. **API Endpoint**: Add to `api.py`
2. **UI Component**: Add to `streamlit_app.py`
3. **Model Logic**: Update `models/train.py`

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings to functions
- Keep functions focused and small

### Testing

```bash
# Run API tests
pytest tests/test_api.py

# Run app tests
pytest tests/test_app.py
```

## Dependencies

See `requirements.txt` for full list:
- FastAPI - Web framework
- Streamlit - UI framework
- Pandas - Data manipulation
- Scikit-learn - ML algorithms
- Plotly - Visualizations
