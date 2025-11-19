#!/usr/bin/env python3
"""
Video Frame to Images Converter
Extracts all frames from a video file and saves them as individual images.
Usage: python main.py <input_video> <output_directory>
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path
from typing import Optional
import re
import platform


class VideoFrameExtractor:
    """Extract frames from video files using FFmpeg."""

    def __init__(
        self,
        video_path: str,
        output_dir: str,
        frame_rate: Optional[str] = None,
        format: str = "png",
    ):
        """
        Initialize the video frame extractor.

        Args:
            video_path: Path to the input video file (supports relative or absolute paths, any FFmpeg-compatible format)
            output_dir: Directory to save extracted frames (supports relative or absolute paths)
            frame_rate: Optional FPS rate (e.g., '1' for 1 frame per second, '30' for all frames at 30fps)
            format: Output image format (png, jpg, bmp, webp, etc. - default: png)
        """
        # Convert to absolute paths for clarity
        self.video_path = Path(video_path).expanduser().resolve()
        self.output_dir = Path(output_dir).expanduser().resolve()
        self.frame_rate = frame_rate or "30"  # Default to 30fps
        self.format = format.lower().lstrip(
            "."
        )  # Normalize format (remove leading dot, lowercase)

        # Setup FFmpeg paths
        self.script_dir = Path(__file__).parent
        self.ffmpeg_dir = self.script_dir / "ffmpeg" / "bin"
        self._setup_ffmpeg_paths()

        self._validate_inputs()
        self._create_output_directory()

    def _setup_ffmpeg_paths(self) -> None:
        """Setup FFmpeg binary paths and environment."""
        if self.ffmpeg_dir.exists():
            # Add local ffmpeg to PATH
            ffmpeg_path = str(self.ffmpeg_dir)
            current_path = os.environ.get("PATH", "")
            os.environ["PATH"] = ffmpeg_path + os.pathsep + current_path
            self.ffmpeg_bin = str(self.ffmpeg_dir / "ffmpeg.exe")
            self.ffprobe_bin = str(self.ffmpeg_dir / "ffprobe.exe")
        else:
            # Fallback to system FFmpeg
            self.ffmpeg_bin = "ffmpeg"
            self.ffprobe_bin = "ffprobe"

    def _validate_inputs(self) -> None:
        """Validate input video file exists and is readable."""
        if not self.video_path.exists():
            raise FileNotFoundError(f"Video file not found: {self.video_path}")

        if not self.video_path.is_file():
            raise ValueError(f"Input path is not a file: {self.video_path}")

        # Check if FFmpeg is installed
        try:
            subprocess.run(
                [self.ffmpeg_bin, "-version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
        except FileNotFoundError:
            raise RuntimeError(
                "FFmpeg is not installed or not in PATH. Please install FFmpeg or ensure ffmpeg folder exists."
            )
        except subprocess.CalledProcessError:
            raise RuntimeError("FFmpeg check failed.")

    def _create_output_directory(self) -> None:
        """Create output directory if it doesn't exist."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Output directory: {self.output_dir.absolute()}")

    def _get_video_info(self) -> dict:
        """Get video information (duration, fps, resolution)."""
        try:
            result = subprocess.run(
                [
                    self.ffprobe_bin,
                    "-v",
                    "error",
                    "-select_streams",
                    "v:0",
                    "-show_entries",
                    "stream=duration,r_frame_rate,width,height",
                    "-of",
                    "default=noprint_wrappers=1:nokey=1:noprint_section_header=1",
                    str(self.video_path),
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )

            lines = result.stdout.strip().split("\n")
            if len(lines) >= 4:
                duration = float(lines[0]) if lines[0] else 0
                fps_str = lines[1]
                # Parse fps like "30/1" or "29.97"
                fps = eval(fps_str) if "/" in fps_str else float(fps_str)
                width = int(lines[2]) if lines[2] else 0
                height = int(lines[3]) if lines[3] else 0

                return {
                    "duration": duration,
                    "fps": fps,
                    "width": width,
                    "height": height,
                }
        except (subprocess.CalledProcessError, ValueError, IndexError):
            print("Warning: Could not retrieve video information")

        return {"duration": 0, "fps": 0, "width": 0, "height": 0}

    def extract_frames(self, verbose: bool = True) -> bool:
        """
        Extract all frames from the video.

        Args:
            verbose: Print progress information

        Returns:
            True if successful, False otherwise
        """
        # Get video info
        video_info = self._get_video_info()

        if verbose:
            print(f"Processing video: {self.video_path.name}")
            if video_info["duration"]:
                print(f"Duration: {video_info['duration']:.2f}s")
                print(f"FPS: {video_info['fps']:.2f}")
                print(f"Resolution: {video_info['width']}x{video_info['height']}")
            print(f"Extracting frames at {self.frame_rate} fps as .{self.format}...")

        # Output pattern for frames
        output_pattern = str(self.output_dir / f"frame_%06d.{self.format}")

        # Build FFmpeg command
        # -vf fps=X sets the frame extraction rate
        # -start_number 0 starts frame numbering at 0
        cmd = [
            self.ffmpeg_bin,
            "-i",
            str(self.video_path),
            "-vf",
            f"fps={self.frame_rate}",
            "-start_number",
            "0",
            output_pattern,
        ]

        try:
            # Run FFmpeg with progress
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

            # Read stderr for progress information
            _, stderr = process.communicate()

            if process.returncode != 0:
                print(f"FFmpeg error: {stderr}")
                return False

            # Count extracted frames
            extracted_frames = len(list(self.output_dir.glob(f"frame_*.{self.format}")))

            if verbose:
                print(f"\n✓ Successfully extracted {extracted_frames} frames")
                print(f"Frames saved to: {self.output_dir.absolute()}")

            return True

        except Exception as e:
            print(f"Error during frame extraction: {e}")
            return False


def find_video_files(folder_path: Path) -> list:
    """
    Find all video files in a folder.

    Args:
        folder_path: Path to the folder to search

    Returns:
        List of video file paths
    """
    video_extensions = {
        ".mp4",
        ".mov",
        ".avi",
        ".mkv",
        ".webm",
        ".flv",
        ".wmv",
        ".m4v",
        ".mpg",
        ".mpeg",
        ".3gp",
        ".m2ts",
        ".mts",
        ".ts",
        ".vob",
        ".f4v",
        ".asf",
        ".rm",
        ".rmvb",
        ".ogv",
        ".mxf",
        ".gif",
    }

    video_files = []
    for file in folder_path.rglob("*"):
        if file.is_file() and file.suffix.lower() in video_extensions:
            video_files.append(file)

    return sorted(video_files)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Extract frames from a video file or all videos in a folder and save as images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py video.mp4 output/
  python main.py video.mp4 output/ --fps 30
  python main.py video.mp4 output/ --fps 1
  python main.py video.mp4 output/ --format jpg
  python main.py video.mov output/ --fps 15 --format webp
  
Folder input (processes all videos):
  python main.py videos_folder/ output/
  python main.py videos_folder/ output/ --fps 10 --format jpg
        """,
    )

    parser.add_argument(
        "input", help="Path to input video file or folder containing videos"
    )

    parser.add_argument("output", help="Output directory for extracted frames")

    parser.add_argument(
        "--fps",
        type=str,
        default=None,
        help="Frames per second to extract (default: 30)",
    )

    parser.add_argument(
        "--format",
        type=str,
        default="png",
        help="Output image format (png, jpg, bmp, webp, etc. - default: png)",
    )

    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Suppress verbose output"
    )

    args = parser.parse_args()

    try:
        input_path = Path(args.input).expanduser().resolve()
        output_base = Path(args.output).expanduser().resolve()

        # Check if input is a folder or a file
        if input_path.is_dir():
            # Process all videos in the folder
            video_files = find_video_files(input_path)

            if not video_files:
                print(f"No video files found in: {input_path}")
                sys.exit(1)

            if not args.quiet:
                print(f"Found {len(video_files)} video file(s) in {input_path.name}/")

            failed_videos = []

            for idx, video_file in enumerate(video_files, 1):
                if not args.quiet:
                    print(f"\n[{idx}/{len(video_files)}] Processing: {video_file.name}")

                # Create subdirectory for each video using video filename (without extension)
                video_name = video_file.stem
                video_output_dir = output_base / video_name

                try:
                    extractor = VideoFrameExtractor(
                        video_path=str(video_file),
                        output_dir=str(video_output_dir),
                        frame_rate=args.fps,
                        format=args.format,
                    )

                    success = extractor.extract_frames(verbose=not args.quiet)

                    if not success:
                        failed_videos.append(video_file.name)

                except (FileNotFoundError, ValueError, RuntimeError) as e:
                    print(f"Error processing {video_file.name}: {e}", file=sys.stderr)
                    failed_videos.append(video_file.name)

            # Summary
            if not args.quiet:
                successful = len(video_files) - len(failed_videos)
                print(f"\n{'=' * 50}")
                print(f"Batch processing complete!")
                print(f"Successfully processed: {successful}/{len(video_files)} videos")
                if failed_videos:
                    print(f"Failed videos: {', '.join(failed_videos)}")
                print(f"Output directory: {output_base.absolute()}")

            sys.exit(0 if not failed_videos else 1)

        elif input_path.is_file():
            # Process single video file
            extractor = VideoFrameExtractor(
                video_path=args.input,
                output_dir=args.output,
                frame_rate=args.fps,
                format=args.format,
            )

            success = extractor.extract_frames(verbose=not args.quiet)

            sys.exit(0 if success else 1)

        else:
            raise FileNotFoundError(f"Input path not found: {input_path}")

    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
