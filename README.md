# Video Frames to Images Converter

A powerful, efficient command-line tool to extract frames from video files and save them as individual images using FFmpeg. Supports both single video processing and batch processing of entire folders with multiple video formats.

## Features

- **Single & Batch Processing**: Process individual videos or entire folders with mixed video formats
- **Multiple Format Support**: Handle `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`, `.flv`, `.wmv`, `.m4v`, `.mpg`, `.mpeg`, `.3gp`, and more
- **Flexible Frame Extraction**: Configurable FPS sampling rates or extract every frame
- **Multiple Output Formats**: Save frames as PNG, JPEG, WebP, BMP, TIFF, and other image formats
- **Smart Directory Structure**: Automatic subdirectory creation for batch processing (one folder per video)
- **Recursive Folder Scanning**: Automatically finds all videos in nested subdirectories
- **Detailed Progress Tracking**: Real-time feedback and batch processing summaries
- **Comprehensive Error Handling**: Graceful error reporting with detailed messages
- **FFmpeg Integration**: Works with local bundled FFmpeg or system-installed version
- **Path Flexibility**: Supports relative, absolute, and home directory (`~`) paths

## Requirements

- **Python**: 3.6 or higher
- **FFmpeg**: With ffprobe (video analysis tool)

## Installation & Setup

### Option 1: Use Local FFmpeg (Recommended)

The project includes a local `ffmpeg/` folder with pre-built binaries. The script automatically detects and uses these.

**No additional setup required!** Just run:
```bash
python3 main.py video.mp4 output/
```

### Option 2: Use System-Installed FFmpeg

If you don't have the local FFmpeg folder, install it on your system:

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
- Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- Or use: `choco install ffmpeg`

### Verify Installation

```bash
ffmpeg -version
ffprobe -version
```

## Quick Start

### Single Video
```bash
python3 main.py video.mp4 output/
```

### Batch Process Folder
```bash
python3 main.py videos_folder/ output/
```

## Usage

### Basic Syntax

**Single video:**
```bash
python3 main.py <input_video> <output_directory> [options]
```

**Multiple videos (folder):**
```bash
python3 main.py <input_folder> <output_directory> [options]
```

Supports relative paths, absolute paths, and home directory expansion (`~`).  
When processing a folder, each video gets its own subdirectory in the output folder.

## Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `input` | Path to video file or folder containing videos (required) | - |
| `output` | Output directory for extracted frames (required) | - |
| `--fps` | Frame extraction rate in frames per second | `30` |
| `--format` | Output image format (png, jpg, webp, bmp, etc.) | `png` |
| `-q, --quiet` | Suppress verbose output | Disabled |
| `-h, --help` | Show help message | - |

### Option Details

#### `--fps` (Frame Extraction Rate)
Controls how many frames to extract per second of video:
- **Number** (e.g., `1`, `15`, `30`): Sample that many frames per second
- **`fps=source`**: Extract every single frame the video contains
- **Lower values** = fewer frames (faster, smaller output)
- **Higher values** = more frames (slower, larger output)

**Examples:**
- `--fps 1`: 1 frame per second (10-second video = ~10 frames)
- `--fps 30`: 30 frames per second (10-second video = ~300 frames)
- `--fps fps=source`: All original frames (depends on video's native FPS)

#### `--format` (Output Image Format)
Supported formats: `png`, `jpg`, `jpeg`, `bmp`, `webp`, `tiff`, `gif`, and all FFmpeg-supported image formats.

**Examples:**
- `--format jpg`: Smaller file size, lossy compression
- `--format png`: Larger file size, lossless compression (default)
- `--format webp`: Modern format, good compression
- `--format bmp`: Uncompressed, largest file size

#### `-q, --quiet`
Suppresses verbose output. Useful for scripting and batch operations.

## Examples

### Single Video Processing

**Basic MP4 extraction:**
```bash
python3 main.py video.mp4 output/
```

**Extract from different file formats:**
```bash
python3 main.py video.mov output/          # MOV format
python3 main.py video.mkv output/          # Matroska format
python3 main.py video.webm output/         # WebM format
```

**Different path types:**
```bash
python3 main.py video.mp4 output/                                    # Relative path
python3 main.py /Users/username/Videos/video.mp4 ~/Desktop/frames/  # Absolute path
python3 main.py ~/Videos/video.mov ~/Desktop/frames/                # Home directory
```

**Extract at custom sampling rates:**
```bash
python3 main.py video.mp4 output/ --fps 1              # 1 frame per second
python3 main.py video.mp4 output/ --fps 15             # 15 frames per second
python3 main.py video.mp4 output/ --fps 30             # 30 frames per second (default)
python3 main.py video.mov output/ --fps fps=source     # All frames
```

**Extract as different image formats:**
```bash
python3 main.py video.mp4 output/ --format jpg         # JPEG format
python3 main.py video.mov output/ --format webp        # WebP format
python3 main.py video.mkv output/ --format bmp         # BMP format
```

**Combine FPS and format:**
```bash
python3 main.py video.mp4 output/ --fps 10 --format jpg
python3 main.py video.mov output/ --fps 5 --format webp
```

**Quiet mode (minimal output):**
```bash
python3 main.py video.mp4 output/ -q
python3 main.py video.mp4 output/ --quiet
```

### Batch Processing (Folder)

**Process all videos in a folder:**
```bash
python3 main.py videos_folder/ output/
```
Automatically finds all video files recursively and creates a subdirectory for each.

**Batch process with custom FPS:**
```bash
python3 main.py videos_folder/ output/ --fps 10
python3 main.py videos_folder/ output/ --fps 1          # Thumbnail overview
```

**Batch process with custom format:**
```bash
python3 main.py videos_folder/ output/ --format jpg
python3 main.py videos_folder/ output/ --format webp
```

**Batch process with both FPS and format:**
```bash
python3 main.py videos_folder/ output/ --fps 5 --format jpg
python3 main.py videos_folder/ output/ --fps 15 --format webp
```

**Batch process in quiet mode:**
```bash
python3 main.py videos_folder/ output/ -q
```

**Complex example - nested folders with custom settings:**
```bash
python3 main.py ~/Downloads/videos/ ~/Projects/frames/ --fps 5 --format jpg
```

### Output Structure

#### Single Video
```
output/
  ├── frame_000000.png
  ├── frame_000001.png
  ├── frame_000002.png
  └── ...
```

#### Multiple Videos (Batch Processing)
```
videos_folder/
  ├── intro.mp4
  ├── tutorial.mov
  └── slideshow.mkv

output/
  ├── intro/
  │   ├── frame_000000.png
  │   ├── frame_000001.png
  │   └── ...
  ├── tutorial/
  │   ├── frame_000000.png
  │   ├── frame_000001.png
  │   └── ...
  └── slideshow/
      ├── frame_000000.png
      ├── frame_000001.png
      └── ...
```

## Frame Naming Convention

Frames are numbered sequentially with zero-padding:
- `frame_000000.png`
- `frame_000001.png`
- `frame_000002.png`
- ... and so on

This numbering applies to each video when batch processing. For example:
- `intro/frame_000000.png` (first frame of intro.mp4)
- `tutorial/frame_000000.png` (first frame of tutorial.mov)

## Supported Video Formats

The tool supports all FFmpeg-compatible video formats, including:

| Format | Extension | Notes |
|--------|-----------|-------|
| MPEG-4 | `.mp4` | Most common, widely supported |
| QuickTime | `.mov` | Apple video format |
| Matroska | `.mkv` | Open standard, high quality |
| AVI | `.avi` | Legacy format |
| WebM | `.webm` | Web video format |
| Flash | `.flv` | Older web format |
| Windows Media | `.wmv` | Windows format |
| MPEG | `.mpg`, `.mpeg` | Legacy format |
| 3GPP | `.3gp` | Mobile video format |
| And many more... | | All FFmpeg-supported formats |

## How It Works

### Single Video Processing
1. Validates that the input video file exists and is readable
2. Checks that FFmpeg is installed and accessible
3. Retrieves video metadata (duration, FPS, resolution)
4. Extracts frames using FFmpeg's fps filter at the specified rate
5. Saves extracted frames as images in the output directory
6. Reports the number of successfully extracted frames

### Batch Folder Processing
1. Scans the input folder recursively for all supported video formats
2. For each video found:
   - Creates a subdirectory in the output folder (named after the video)
   - Extracts frames to that subdirectory
   - Reports progress
3. Provides a summary of successfully processed videos and any failures

## Performance Tips

### Choosing FPS
- **Video duration × FPS = total frames**: A 10-second video at `--fps 30` extracts ~300 frames
- **Thumbnails**: Use `--fps 1` for one frame per second (quick overview)
- **Detailed analysis**: Use `--fps 30` or `--fps fps=source` for frame-by-frame inspection
- **Speed**: Lower FPS values extract faster

### Choosing Format
- **PNG** (default): Lossless, larger file size (~100-500KB per frame)
- **JPEG**: Lossy compression, smaller file size (~50-100KB per frame)
- **WebP**: Modern format, good compression (~30-100KB per frame)
- **Storage estimate**: 1-hour video at 30fps = ~108,000 frames
  - PNG: ~10-50GB
  - JPEG: ~5-10GB
  - WebP: ~3-10GB

### Optimization Strategies
- Use `--format jpg` or `--format webp` for storage-constrained environments
- Use lower `--fps` values if speed is critical
- Process large batches overnight or in background
- Monitor disk space before processing long videos

## Troubleshooting

### FFmpeg Not Found
**Problem**: `Error: FFmpeg is not installed or not in PATH`

**Solution**:
1. Ensure FFmpeg is installed: `ffmpeg -version`
2. Check if local `ffmpeg/bin/` folder exists
3. Add FFmpeg to system PATH if using system installation
4. On Windows, restart terminal after installation

### No Video Files Found
**Problem**: `No video files found in: /path/to/folder`

**Solution**:
1. Verify the folder path is correct
2. Check that video files have recognized extensions (.mp4, .mov, etc.)
3. Ensure file permissions allow reading
4. Note: Tool searches recursively in subdirectories

### Video Codec Not Supported
**Problem**: `FFmpeg error: Unknown encoder`

**Solution**:
1. Verify the video format is FFmpeg-compatible (MP4, MOV, MKV, AVI, etc.)
2. Try converting the video using: `ffmpeg -i input.ext output.mp4`
3. Check FFmpeg version: `ffmpeg -version`

### Extraction Is Slow
**Problem**: Frame extraction takes very long

**Solution**:
1. Reduce `--fps` value (e.g., `--fps 1` instead of `--fps 30`)
2. Use `--format jpg` instead of `--format png`
3. Process smaller videos first to test settings
4. For batch operations, run in background: `python3 main.py ... &`

### Out of Disk Space
**Problem**: "No space left on device"

**Solution**:
1. Calculate storage needed:
   - `(video_duration_seconds × fps) × average_frame_size`
   - PNG: ~100-500KB per frame
   - JPEG: ~50-100KB per frame
2. Free up disk space before processing
3. Use lower FPS or JPEG format to reduce output size
4. Process videos in smaller batches

### Folder Processing Errors
**Problem**: Some videos fail, others succeed

**Solution**:
1. Check the summary output for which videos failed
2. Try processing failed videos individually to identify issues
3. Verify codec compatibility with FFmpeg
4. Check file permissions and disk space

### Frame Count Mismatch
**Problem**: Fewer frames extracted than expected

**Solution**:
Remember: `--fps` is sampling rate per second, not total count
- 10-second video at `--fps 1` = ~10 frames (1 per second)
- 10-second video at `--fps 30` = ~300 frames (30 per second)
- To get all frames: use `--fps fps=source`

## Advanced Usage

### Scripting & Automation
```bash
# Batch process with error tracking
python3 main.py input_folder/ output_folder/ -q >> extraction.log 2>&1

# Process multiple folder batches
for folder in batch1 batch2 batch3; do
  python3 main.py "$folder/" "output/$folder/" --fps 5 --format jpg
done
```

### Integration with Other Tools
```bash
# Extract frames then compress
python3 main.py video.mp4 frames/ --format jpg && zip -r frames.zip frames/

# Extract and resize frames (requires ImageMagick)
python3 main.py video.mp4 frames/ && mogrify -resize 50% frames/*.jpg
```

## Project Structure

```
VideoFramesToImages/
├── main.py              # Main script
├── README.md            # This file
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore file
└── ffmpeg/             # Optional local FFmpeg binaries
    ├── bin/
    │   ├── ffmpeg.exe
    │   └── ffprobe.exe
    └── ...
```

## License

This project is provided as-is for personal and educational use.

## Contributing

Feel free to report issues, suggest improvements, or submit enhancements.

## Support

For issues or questions:
- Check the Troubleshooting section above
- Verify FFmpeg installation: `ffmpeg -version`
- Test with a small video file first
- Try `python3 main.py --help` for command options
