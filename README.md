# WebP to WebM Converter

Two scripts for converting animated WebP files to needed Telegram Sticers Webm format

## Requirements

- Python 3.x
- ffmpeg
- ImageMagick (only for `convert_webp_to_webm.py`)

## Scripts

### 1. convert_webp_to_webm_simple.py
Simple converter that:
- Converts WebP files directly using ffmpeg
- Limits output file size to 256 KB

### 2. convert_webp_to_webm.py
Advanced converter that:
- First tries direct ffmpeg conversion
- Falls back to ImageMagick (WebP → GIF → WebM) if needed
- Limits output file size to 256 KB

## Usage

1. Place WebP files in the script directory
2. Run the desired script:
```bash
python convert_webp_to_webm_simple.py
# or
python convert_webp_to_webm.py
```
3. Enter specific filename or press Enter to convert all files
4. Converted files will appear in the `webm_output` folder
