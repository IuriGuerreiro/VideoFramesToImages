# Video Frames to Images Converter

Extract all frames from a video file and save them as individual images using FFmpeg.

## Features

- Extract frames from any video format supported by FFmpeg
- Configurable frame extraction rate (FPS)
- Progress tracking and detailed output
- Automatic output directory creation
- Comprehensive error handling
- Command-line argument parsing
- Works with local FFmpeg binaries or system-installed FFmpeg

## Requirements

- Python 3.6+
- FFmpeg (with ffprobe)

## Installation & Setup

### Option 1: Use Local FFmpeg (Recommended)

The project includes a local `ffmpeg/` folder with pre-built binaries. The script will automatically use these if available.

**No additional setup needed!** Just run the script:
```bash
python main.py video.mp4 output/
```

### Option 2: Use System-Installed FFmpeg

If you don't have the local FFmpeg folder, install FFmpeg on your system:

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
- Download from https://ffmpeg.org/download.html
- Or use: `choco install ffmpeg`

### Verify Installation

```bash
ffmpeg -version
ffprobe -version
```

## Usage

Basic usage:
```bash
python main.py <input_video> <output_directory>
```

Supports both relative and absolute paths, including home directory expansion (`~`).

### Examples

**MP4 with relative paths:**
```bash
python main.py video.mp4 output/
```

**MOV with relative paths:**
```bash
python main.py video.mov output/
```

**Full absolute path:**
```bash
python main.py /Users/username/Videos/video.mp4 /Users/username/Desktop/frames/
```

**Home directory path:**
```bash
python main.py ~/Videos/video.mov ~/Desktop/frames/
```

**Sample 1 frame per second from the video:**
```bash
python main.py video.mp4 output/ --fps 1
```
(If video is 60 seconds long, extracts ~60 frames)

**Extract every single frame the video contains:**
```bash
python main.py video.mov output/ --fps fps=source
```

**Sample at 15 fps:**
```bash
python main.py video.mp4 output/ --fps 15
```
(If video is 10 seconds at 30fps original, extracts ~150 frames)

**Extract as JPEG format:**
```bash
python main.py video.mp4 output/ --format jpg
```

**Extract as WebP format:**
```bash
python main.py video.mov output/ --format webp
```

**Combine fps and format:**
```bash
python main.py video.mp4 output/ --fps 10 --format jpg
```

**Quiet mode (no verbose output):**
```bash
python main.py video.mp4 output/ -q
```

## Output

Extracted frames are saved with the naming pattern (format depends on `--format` option):
- `frame_000000.png` (default)
- `frame_000001.png`
- `frame_000002.png`
- etc.

Or with other formats:
- `frame_000000.jpg` (with `--format jpg`)
- `frame_000000.webp` (with `--format webp`)
- `frame_000000.bmp` (with `--format bmp`)

## Options

- `input`: Path to input video file (required)
  - Supports: `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`, `.flv`, and all FFmpeg-compatible formats
  - Accepts: relative paths, absolute paths, and home directory (`~`) paths
- `output`: Output directory for extracted frames (required)
  - Accepts: relative paths, absolute paths, and home directory (`~`) paths
  - Directory will be created automatically if it doesn't exist
- `--fps`: Sampling rate in frames per second (default: 30)
  - Controls how many frames to sample from the video per second
  - A number (e.g., `1`, `15`, `30`) means sample that many frames per second of video
  - `fps=source` extracts every frame the video contains
  - Lower values = fewer frames extracted (faster, smaller output)
  - Higher values = more frames extracted (slower, larger output)
- `--format`: Output image format (default: png)
  - Supports: `png`, `jpg`, `jpeg`, `bmp`, `webp`, `tiff`, and all FFmpeg-supported image formats
  - Examples: `--format jpg`, `--format webp`, `--format bmp`
- `-q, --quiet`: Suppress verbose output

## How It Works

1. Validates that the input video exists and is readable
2. Checks that FFmpeg is installed
3. Retrieves video information (duration, FPS, resolution)
4. Extracts frames using FFmpeg's fps filter
5. Saves frames as images (format specified by `--format` option) to the output directory
6. Reports the number of successfully extracted frames

## Performance Tips

- **Video length + FPS = total frames**: A 10-second video at `--fps 30` will extract ~300 frames
- **Lower FPS = faster extraction**: Use `--fps 1` for a thumbnail overview (1 frame per second)
- **Higher FPS = more frames**: Use `--fps 30` or `--fps fps=source` for detailed frame-by-frame analysis
- **Format choice matters**: PNG is lossless but larger; JPEG is smaller but lossy
- Extraction speed depends on video resolution and your system specs

## Troubleshooting

### FFmpeg not found
Make sure FFmpeg is installed and in your system PATH.

### Video codec not supported
Ensure you're using a video format that FFmpeg supports (MP4, AVI, MKV, MOV, etc.)

### Out of disk space
Large videos with high fps settings can generate many frames. Ensure you have enough free space.
- Example: 1-hour video at 30fps = ~108,000 frames. At ~100KB per PNG, that's ~10GB of storage.

### Slow extraction
Try reducing the `--fps` value to extract fewer frames, or use `--format jpg` for smaller files.

### Too many/too few frames
Remember: `--fps` controls sampling rate per second of video, not total frame count.
- For a 10-second video: `--fps 1` = ~10 frames, `--fps 30` = ~300 frames, `--fps fps=source` = depends on original video fps
