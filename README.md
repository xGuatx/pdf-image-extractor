# PDF Image Extractor - Docker Tool

Docker-based tool to extract images from PDF files using Python and various PDF libraries.

## Description

Automated image extraction from PDF documents, supporting various image formats and batch processing.

## Prerequisites

- Docker
- Docker Compose

## Installation

```bash
# Build and start
docker-compose up -d
```

## Usage

### Basic Extraction

```bash
# Extract from single PDF
docker-compose run --rm pdf-extractor \
  python extract.py input.pdf output_folder/
```

### Batch Processing

```bash
# Extract from all PDFs in folder
docker-compose run --rm pdf-extractor \
  python batch_extract.py /pdfs/ /output/
```

## Configuration

### docker-compose.yml Example

```yaml
services:
  pdf-extractor:
    build: .
    volumes:
      - ./pdfs:/pdfs
      - ./output:/output
```

### Dockerfile

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install --no-cache-dir \
    PyPDF2 \
    pdf2image \
    Pillow \
    pdfplumber

WORKDIR /app
COPY scripts/ .

CMD ["python", "extract.py"]
```

## Features

- Extract all images from PDF
- Preserve original image quality
- Support for multiple formats (JPEG, PNG, TIFF)
- Batch processing
- Metadata extraction
- Image quality filtering

## Scripts

### extract.py

Basic extraction script:
```python
import sys
from pdf2image import convert_from_path
from PIL import Image

def extract_images(pdf_path, output_folder):
    # Convert PDF pages to images
    images = convert_from_path(pdf_path)

    for i, image in enumerate(images):
        image.save(f'{output_folder}/page_{i+1}.png', 'PNG')
        print(f'Extracted page {i+1}')

if __name__ == '__main__':
    pdf_path = sys.argv[1]
    output_folder = sys.argv[2]
    extract_images(pdf_path, output_folder)
```

### Advanced Options

```bash
# Extract with DPI setting
docker-compose run --rm pdf-extractor \
  python extract.py input.pdf output/ --dpi 300

# Extract specific pages
docker-compose run --rm pdf-extractor \
  python extract.py input.pdf output/ --pages 1-5,10

# Extract only high-quality images
docker-compose run --rm pdf-extractor \
  python extract.py input.pdf output/ --min-size 1000x1000
```

## Output Formats

### Supported Formats
- PNG (lossless)
- JPEG (compressed)
- TIFF (high quality)
- WebP

### Quality Settings

```python
# High quality JPEG
image.save('output.jpg', 'JPEG', quality=95)

# PNG with compression
image.save('output.png', 'PNG', optimize=True)
```

## Use Cases

- Extract diagrams from technical documents
- Recover images from scanned PDFs
- Batch process document archives
- Create image galleries from PDF collections
- Extract figures for presentations

## Advanced Features

### Metadata Extraction

```python
import PyPDF2

def get_pdf_info(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        info = reader.metadata
        print(f"Pages: {len(reader.pages)}")
        print(f"Author: {info.author}")
        print(f"Title: {info.title}")
```

### Image Filtering

```python
def filter_small_images(images, min_width=500, min_height=500):
    return [img for img in images
            if img.width >= min_width and img.height >= min_height]
```

### OCR Integration

```python
import pytesseract

def extract_text_from_image(image):
    return pytesseract.image_to_string(image)
```

## Performance

### Large PDFs

For large PDFs (100+ pages):
```bash
# Process in chunks
docker-compose run --rm pdf-extractor \
  python extract.py large.pdf output/ --chunk-size 10
```

### Memory Optimization

```python
# Process one page at a time
for page_num in range(len(pdf_pages)):
    image = convert_from_path(pdf_path, first_page=page_num, last_page=page_num)
    # Process and save
    del image  # Free memory
```

## Troubleshooting

### Dependency Issues

```bash
# Rebuild container
docker-compose build --no-cache
```

### Permission Errors

```bash
# Fix output folder permissions
chmod -R 777 ./output
```

### Low Quality Output

```bash
# Increase DPI
docker-compose run --rm pdf-extractor \
  python extract.py input.pdf output/ --dpi 600
```

## Common Commands

```bash
# Extract all images
docker-compose run --rm pdf-extractor python extract.py /pdfs/document.pdf /output/

# Batch process folder
docker-compose run --rm pdf-extractor python batch_extract.py /pdfs/ /output/

# View help
docker-compose run --rm pdf-extractor python extract.py --help
```

## Automation

### Bash Script

```bash
#!/bin/bash
# Extract images from all PDFs in directory

for pdf in /pdfs/*.pdf; do
    filename=$(basename "$pdf" .pdf)
    mkdir -p "/output/$filename"
    docker-compose run --rm pdf-extractor \
        python extract.py "$pdf" "/output/$filename/"
done
```

## Best Practices

- Use high DPI (300+) for print-quality
- Filter small/low-quality images
- Organize output by PDF name
- Clean up temporary files
- Validate PDF before processing

## Libraries Used

- **PyPDF2**: PDF manipulation
- **pdf2image**: PDF to image conversion
- **Pillow**: Image processing
- **pdfplumber**: Advanced PDF parsing

## Resources

- [PyPDF2 Documentation](https://pypdf2.readthedocs.io/)
- [pdf2image](https://github.com/Belval/pdf2image)
- [Pillow Documentation](https://pillow.readthedocs.io/)

## License

Personal project - Private use
