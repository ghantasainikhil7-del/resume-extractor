# Resume Extractor

A Python application to extract and parse resume data from multiple documents across different professional categories.

## Project Structure

- `app.py` - Main Flask/web application
- `resume_extractor.py` - Resume extraction logic
- `resume_parser.py` - Resume parsing logic
- `main_runner.py` - Main execution script
- `os_walk.py` - Utility for directory traversal
- `test_extractor.py` - Tests for extractor
- `test_parser.py` - Tests for parser
- `data/` - Input resume data organized by profession
- `output/` - Processed output files
- `templates/` - HTML templates for the web interface

## Features

- Extract resume information from documents
- Parse resume data into structured format
- Support for multiple professional categories
- Web interface for easy access
- CSV and JSON output formats

## Installation

1. Create a virtual environment:
```bash
python -m venv .venv
```

2. Activate the virtual environment:
- Windows: `.venv\Scripts\activate`
- Linux/Mac: `source .venv/bin/activate`

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the web application:
```bash
python app.py
```

Or run the main runner:
```bash
python main_runner.py
```

## Testing

Run tests for extractor:
```bash
python test_extractor.py
```

Run tests for parser:
```bash
python test_parser.py
```

## Output

- CSV format: `output/resume_data.csv`
- JSONL format: `output/resumes.jsonl`

## License

MIT License
