import os
import subprocess
from pathlib import Path

def convert_webp_to_webm():
    current_dir = Path('.')
    output_dir = current_dir / 'webm_output'
    output_dir.mkdir(exist_ok=True)
    webp_files = list(current_dir.glob('*.webp'))
    if not webp_files:
        print("No WebP files found in current directory.")
        return
    print(f"Found {len(webp_files)} WebP files.")
    failed_files = []
    for webp_file in webp_files:
        output_file = output_dir / webp_file.with_suffix('.webm').name
        print(f"Converting {webp_file} to {output_file}...")
        try:
            subprocess.run([
                'ffmpeg', '-y',
                '-hide_banner',
                '-loglevel', 'error',
                '-i', str(webp_file),
                '-vf', 'scale=512:512:force_original_aspect_ratio=decrease,pad=512:512:-1:-1:color=black',
                '-c:v', 'libvpx-vp9',
                '-crf', '30',
                '-b:v', '0',
                '-fs', '256k',
                str(output_file)
            ], check=True)
            print(f"Successfully converted {webp_file}.")
        except subprocess.CalledProcessError:
            print(f"Failed to convert {webp_file}.")
            failed_files.append(str(webp_file))
        except FileNotFoundError:
            print("Error: ffmpeg is not installed. Please install ffmpeg and try again.")
            return
    print("----------------------")
    if failed_files:
        print("Failed to convert the following files:")
        for f in failed_files:
            print(f)
    else:
        print("All files converted successfully.")
    print("----------------------")
    print("press Enter to exit")
    input()

if __name__ == "__main__":
    print("WebP to WebM Simple Converter")
    print("----------------------")
    convert_webp_to_webm() 