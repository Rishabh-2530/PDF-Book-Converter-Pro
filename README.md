# PDF Book Converter Pro v2.0

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-6.7%2B-green)](https://doc.qt.io/qtforpython/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

A professional Windows desktop application for converting scanned and digital PDF books into editable formats while preserving layout, formulas, diagrams, and images.

## Features

### Version 2.0 (Current)
- ✅ Modern PDF Viewer (Adobe Acrobat-style UI)
- ✅ Smooth Navigation (First, Previous, Next, Last, Go To Page)
- ✅ Advanced Zoom (Fit Width, Fit Page, 25%-500% custom)
- ✅ High-quality Page Rendering with Caching
- ✅ Export to PNG, JPEG, WEBP, TIFF
- ✅ OCR Support (English, Hindi, Math)
- ✅ PDF to Word Conversion

### Future Versions
- Formula Detection (v2.5)
- Diagram Detection (v2.5)
- AI Layout Detection (v3.0)
- Chapter Summarization (v3.0)
- Translation (v3.0)

## Technology Stack

- **Language**: Python 3.12+
- **GUI**: PySide6 (Qt6)
- **PDF Processing**: PyMuPDF (fitz)
- **OCR**: Tesseract, EasyOCR
- **Document Export**: python-docx
- **Image Processing**: Pillow, OpenCV
- **AI Models**: LayoutParser, Detectron2

## Project Structure

```
PDF_Book_Converter_Pro/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── engine/                 # Core functionality
│   ├── pdf_manager.py     # PDF loading and page extraction
│   ├── preview_widget.py  # Page rendering
│   ├── export_engine.py   # Export to various formats
│   ├── zoom_manager.py    # Zoom control logic
│   ├── ocr_engine.py      # OCR operations
│   ├── converter.py       # PDF to Word conversion
│   └── cache_manager.py   # Page caching
├── ui/                     # User interface
│   ├── main_window.py     # Main application window
│   ├── preview_widget.py  # PDF preview widget
│   ├── toolbar.py         # Toolbar controls
│   ├── statusbar.py       # Status bar
│   └── dialogs.py         # Dialog windows
├── assets/                 # Icons and styles
├── temp/                   # Temporary files
├── output/                 # Exported files
└── logs/                   # Application logs
```

## Installation

### Prerequisites
- Python 3.12 or higher
- Windows 10/11
- Tesseract OCR (optional, for OCR features)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Rishabh-2530/PDF-Book-Converter-Pro.git
cd PDF-Book-Converter-Pro
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python main.py
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Open PDF |
| `Ctrl+S` | Save PDF |
| `Ctrl+Plus` | Zoom In |
| `Ctrl+Minus` | Zoom Out |
| `Left Arrow` | Previous Page |
| `Right Arrow` | Next Page |
| `Home` | First Page |
| `End` | Last Page |
| `Ctrl+Mouse Wheel` | Smooth Zoom |

## Usage

1. **Open a PDF**: Click "Open" button or press `Ctrl+O`
2. **Navigate**: Use arrow keys or navigation buttons
3. **Zoom**: Use `Ctrl+Mouse Wheel` or zoom buttons
4. **Export**: Select pages and choose export format
5. **OCR**: Click OCR button to extract text
6. **Convert**: Use Convert button for PDF to Word

## Development

### Git Workflow
```
main
├── develop
│   ├── feature/viewer
│   ├── feature/zoom
│   ├── feature/export
│   ├── feature/ocr
│   ├── feature/converter
│   └── feature/ai
```

### Code Standards
- Follow PEP8
- Use type hints
- Write docstrings
- MVC architecture
- Log all operations
- No global variables

### Testing
```bash
pytest tests/
```

## Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -am 'Add feature'`
3. Push branch: `git push origin feature/your-feature`
4. Create Pull Request

## License

MIT License - See LICENSE file for details

## Author

**Rishabh-2530** - [GitHub Profile](https://github.com/Rishabh-2530)

## Support

For issues, questions, or suggestions, please open a GitHub issue.
