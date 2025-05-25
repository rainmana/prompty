# 🧠 AI Prompt Library

A modern, dark-themed Streamlit application for managing and organizing AI prompts. Built specifically for security professionals and developers who need a structured way to store, categorize, and deploy AI prompts.

## Features

### Core Functionality
- **Modern Dark UI**: Sleek, professional interface optimized for extended use
- **SQLite Database**: Lightweight, embedded database requiring no external dependencies
- **Full CRUD Operations**: Create, Read, Update, Delete prompts with ease
- **Advanced Search**: Full-text search across titles, descriptions, and content
- **Category Management**: Organize prompts by categories with custom colors
- **Tag System**: Flexible tagging for cross-category organization
- **Import/Export**: JSON-based backup and migration capabilities

### Security Professional Features
- **Penetration Testing Templates**: Pre-built categories for security assessments
- **Code Generation Prompts**: Specialized prompts for security tool development
- **Analysis Templates**: Structured prompts for vulnerability analysis
- **Deployment Ready**: Single container deployment for isolated environments

### Technical Specifications
- **Framework**: Streamlit 1.28.1
- **Database**: SQLite 3
- **Container**: Single Docker container deployment
- **UI Theme**: Custom CSS with modern dark theme
- **Typography**: Inter font family for improved readability

## Quick Start

### Using Docker (Recommended)

1. **Clone and Build**:
```bash
git clone <repository-url>
cd ai-prompt-library
docker-compose up -d
```

2. **Access Application**:
   - Open browser to `http://localhost:8501`
   - Application will be running in dark mode by default

### Manual Installation

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run Application**:
```bash
streamlit run app.py
```

## Usage Guide

### Adding Prompts
1. Navigate to "Add New Prompt" in the sidebar
2. Fill in required fields (Title and Content)
3. Select appropriate category and add tags
4. Click "Add Prompt" to save

### Managing Categories
- Default categories include: General, Creative Writing, Code Generation, Analysis, Security, Business
- Access "Manage Categories" to add custom categories
- Each category supports custom color coding

### Search and Filter
- Use the sidebar search box for full-text search
- Filter by category using the dropdown
- Results update in real-time

### Import/Export
- Export all prompts to JSON format
- Import prompts from JSON files
- Useful for backup and migration between environments

## Database Schema

### Prompts Table
```sql
CREATE TABLE prompts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    content TEXT NOT NULL,
    category TEXT NOT NULL,
    tags TEXT,  -- JSON array
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usage_count INTEGER DEFAULT 0,
    rating REAL DEFAULT 0.0
);
```

### Categories Table
```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    color TEXT DEFAULT '#6366f1'
);
```

## Configuration

### Environment Variables
- `STREAMLIT_SERVER_PORT`: Default 8501
- `STREAMLIT_SERVER_ADDRESS`: Default 0.0.0.0
- `STREAMLIT_BROWSER_GATHER_USAGE_STATS`: Set to false for privacy

### Database Location
- SQLite database stored in `/app/data/prompts.db` within container
- Volume mounted to `./data` on host for persistence

## Security Considerations

### Data Protection
- Database stored locally with no external connections
- No telemetry or usage statistics collection
- Suitable for air-gapped environments

### Access Control
- No built-in authentication (designed for single-user or trusted environments)
- For multi-user environments, deploy behind reverse proxy with authentication

## Customization

### Theme Customization
- CSS variables defined in `load_css()` function
- Modify color scheme by updating CSS custom properties
- Supports full theme customization

### Database Extensions
- SQLite database can be extended with additional tables
- Current schema supports future enhancements (rating, usage tracking)

## Troubleshooting

### Common Issues

1. **Port Already in Use**:
   - Change port in docker-compose.yml
   - Default: 8501

2. **Database Permissions**:
   - Ensure `./data` directory has write permissions
   - Docker container runs as non-root user

3. **Memory Issues**:
   - SQLite handles large datasets efficiently
   - Consider pagination for 10,000+ prompts

### Performance Optimization
- Database indexes automatically created for search fields
- Full-text search optimized for response time
- Lazy loading implemented for large prompt collections

## Development

### File Structure
```
ai-prompt-library/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── Dockerfile         # Container configuration
├── docker-compose.yml # Deployment configuration
├── README.md          # This file
└── data/             # Database storage (created on first run)
    └── prompts.db    # SQLite database
```

### Contributing
- Follow PEP 8 style guidelines
- Add type hints for new functions
- Test database operations thoroughly
- Ensure dark theme compatibility for UI changes

## License

MIT License - See LICENSE file for details

---

**Built for Security Professionals** | **Optimized for ADHD/Autism** | **Dark Mode First**
