import os
import subprocess
from pathlib import Path

def convert_webp_to_webm(specific_file=None):
    # Get current directory
    current_dir = Path('.')
    
    # Create output directory if it doesn't exist
    output_dir = current_dir / 'webm_output'
    output_dir.mkdir(exist_ok=True)
    
    # Find WebP files based on input
    if specific_file:
        file_path = current_dir / specific_file
        if not file_path.exists():
            print(f"Error: File '{specific_file}' not found.")
            return
        if not file_path.suffix.lower() == '.webp':
            print(f"Error: File '{specific_file}' is not a WebP file.")
            return
        webp_files = [file_path]
    else:
        webp_files = list(current_dir.glob('*.webp'))
    
    if not webp_files:
        print("No WebP files found in current directory.")
        return
    
    print(f"Found {len(webp_files)} WebP files.")
    
    for webp_file in webp_files:
        output_file = output_dir / webp_file.with_suffix('.webm').name
        print(f"Converting {webp_file} to {output_file}...")
        
        ffmpeg_success = False
        try:
            # Try direct ffmpeg conversion with file size limit
            subprocess.run([
                'ffmpeg', '-y',
                '-hide_banner',
                '-loglevel', 'error',
                '-i', str(webp_file),
                '-c:v', 'libvpx-vp9',
                '-crf', '30',
                '-b:v', '0',
                '-fs', '256k',
                str(output_file)
            ], check=True)
            print(f"Successfully converted {webp_file} via ffmpeg.")
            ffmpeg_success = True
        except subprocess.CalledProcessError:
            print(f"Direct ffmpeg conversion failed for {webp_file}. Trying via GIF...")
        except FileNotFoundError:
            print("Error: ffmpeg is not installed. Please install ffmpeg and try again.")
            return
        
        if not ffmpeg_success:
            temp_gif = current_dir / 'temp_anim.gif'
            try:
                # webp -> gif via ImageMagick
                subprocess.run([
                    'magick', 'convert',
                    '-quiet',
                    str(webp_file),
                    str(temp_gif)
                ], check=True)
                # gif -> webm via ffmpeg with file size limit
                subprocess.run([
                    'ffmpeg', '-y',
                    '-hide_banner',
                    '-loglevel', 'error',
                    '-i', str(temp_gif),
                    '-c:v', 'libvpx-vp9',
                    '-crf', '30',
                    '-b:v', '0',
                    '-fs', '256k',
                    str(output_file)
                ], check=True)
                print(f"Successfully converted {webp_file} via GIF fallback.")
            except subprocess.CalledProcessError as e:
                print(f"Conversion failed for {webp_file}: {e}")
            except FileNotFoundError as e:
                print(f"Error: Required tool not installed: {e}")
            finally:
                if temp_gif.exists():
                    try:
                        temp_gif.unlink()
                    except Exception:
                        pass

if __name__ == "__main__":
    print("WebP to WebM Converter")
    print("----------------------")
    print("Enter the name of the WebP file to convert (or press Enter to convert all WebP files):")
    
    user_input = input().strip()
    
    if user_input:
        convert_webp_to_webm(user_input)
    else:
        convert_webp_to_webm()
    
    print("----------------------")
    print("press Enter to exit")
    input()