#!/usr/bin/env python3
"""
Video Contact Sheet Generator

Automatically generates contact sheet thumbnails for videos by extracting
scene-representative frames using HSV histogram difference detection.
"""

import argparse
import cv2
import numpy as np
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont
import math


class VideoContactSheet:
    """Generates contact sheets from video files with scene change detection."""
    
    def __init__(self, max_frames=16, cols=4, scene_thresh=0.3, threads=4):
        """
        Initialize the contact sheet generator.
        
        Args:
            max_frames (int): Maximum number of frames to extract
            cols (int): Number of columns in the contact sheet grid
            scene_thresh (float): Threshold for scene change detection (0.0-1.0)
            threads (int): Number of threads for processing
        """
        self.max_frames = max_frames
        self.cols = cols
        self.scene_thresh = scene_thresh
        self.threads = threads
        
    def calculate_histogram(self, frame):
        """Calculate HSV histogram for a frame."""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1, 2], None, [50, 60, 60], [0, 180, 0, 256, 0, 256])
        return cv2.normalize(hist, hist).flatten()
    
    def detect_scene_changes(self, video_path):
        """
        Detect scene changes in video using HSV histogram difference.
        
        Args:
            video_path (str): Path to the video file
            
        Returns:
            list: List of (frame_number, frame_image) tuples for scene changes
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video file: {video_path}")
        
        frames = []
        prev_hist = None
        frame_count = 0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Always include first frame
        ret, first_frame = cap.read()
        if ret:
            frames.append((0, first_frame.copy()))
            prev_hist = self.calculate_histogram(first_frame)
            frame_count += 1
        
        # Skip frames to avoid processing every single frame for long videos
        skip_frames = max(1, total_frames // (self.max_frames * 10))
        
        while len(frames) < self.max_frames and ret:
            # Skip frames for efficiency
            for _ in range(skip_frames):
                ret, frame = cap.read()
                frame_count += 1
                if not ret:
                    break
            
            if not ret:
                break
                
            current_hist = self.calculate_histogram(frame)
            
            # Calculate histogram difference
            if prev_hist is not None:
                diff = cv2.compareHist(prev_hist, current_hist, cv2.HISTCMP_CORREL)
                
                # If correlation is low (different scenes), add frame
                if diff < (1 - self.scene_thresh):
                    frames.append((frame_count, frame.copy()))
                    prev_hist = current_hist
        
        cap.release()
        
        # If we don't have enough frames, add evenly spaced frames
        if len(frames) < self.max_frames:
            cap = cv2.VideoCapture(video_path)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            step = total_frames // (self.max_frames - len(frames) + 1)
            
            existing_frame_nums = {f[0] for f in frames}
            
            for i in range(step, total_frames, step):
                if len(frames) >= self.max_frames:
                    break
                if i not in existing_frame_nums:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, i)
                    ret, frame = cap.read()
                    if ret:
                        frames.append((i, frame.copy()))
            
            cap.release()
        
        return frames[:self.max_frames]
    
    def get_video_metadata(self, video_path):
        """Extract basic metadata from video file."""
        cap = cv2.VideoCapture(video_path)
        
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        duration = frame_count / fps if fps > 0 else 0
        
        # Try to get codec information (fourcc)
        fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
        codec = "".join([chr((fourcc >> 8 * i) & 0xFF) for i in range(4)])
        
        cap.release()
        
        return {
            'duration': duration,
            'resolution': f"{width}x{height}",
            'codec': codec.strip(),
            'fps': fps
        }
    
    def create_contact_sheet(self, frames, metadata, output_path):
        """
        Create the contact sheet from extracted frames.
        
        Args:
            frames (list): List of (frame_number, frame_image) tuples
            metadata (dict): Video metadata
            output_path (str): Path for output image
        """
        if not frames:
            raise ValueError("No frames to create contact sheet")
        
        # Calculate grid dimensions
        rows = math.ceil(len(frames) / self.cols)
        
        # Resize frames to thumbnail size
        thumb_width, thumb_height = 240, 180
        thumbnails = []
        
        for frame_num, frame in frames:
            # Convert BGR to RGB for PIL
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            thumb = Image.fromarray(frame_rgb)
            thumb = thumb.resize((thumb_width, thumb_height), Image.Resampling.LANCZOS)
            thumbnails.append(thumb)
        
        # Create contact sheet
        margin = 10
        footer_height = 60
        
        contact_width = self.cols * thumb_width + (self.cols + 1) * margin
        contact_height = rows * thumb_height + (rows + 1) * margin + footer_height
        
        contact_sheet = Image.new('RGB', (contact_width, contact_height), 'white')
        
        # Place thumbnails
        for i, thumb in enumerate(thumbnails):
            row = i // self.cols
            col = i % self.cols
            
            x = margin + col * (thumb_width + margin)
            y = margin + row * (thumb_height + margin)
            
            contact_sheet.paste(thumb, (x, y))
        
        # Add footer with metadata
        self._add_footer(contact_sheet, metadata, footer_height)
        
        # Save as JPEG
        contact_sheet.save(output_path, 'JPEG', quality=90)
    
    def _add_footer(self, image, metadata, footer_height):
        """Add metadata footer to the contact sheet."""
        draw = ImageDraw.Draw(image)
        
        # Try to use a default font, fall back to basic if not available
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 14)
        except:
            try:
                font = ImageFont.load_default()
            except:
                font = None
        
        # Format metadata text
        duration_str = f"{metadata['duration']:.1f}s"
        text = f"Duration: {duration_str} | Resolution: {metadata['resolution']} | Codec: {metadata['codec']}"
        
        # Calculate text position
        img_width, img_height = image.size
        footer_y = img_height - footer_height + 20
        
        # Draw text
        if font:
            draw.text((20, footer_y), text, fill='black', font=font)
        else:
            draw.text((20, footer_y), text, fill='black')
    
    def generate_contact_sheet(self, video_path, output_path=None):
        """
        Generate a contact sheet for the given video.
        
        Args:
            video_path (str): Path to input video file
            output_path (str): Path for output image (optional)
            
        Returns:
            str: Path to the generated contact sheet
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        if output_path is None:
            base_name = os.path.splitext(os.path.basename(video_path))[0]
            output_path = f"{base_name}_contact_sheet.jpg"
        
        print(f"Analyzing video: {video_path}")
        print(f"Extracting up to {self.max_frames} scene-representative frames...")
        
        # Extract frames with scene detection
        frames = self.detect_scene_changes(video_path)
        print(f"Extracted {len(frames)} frames")
        
        # Get video metadata
        metadata = self.get_video_metadata(video_path)
        
        # Create contact sheet
        print(f"Creating contact sheet: {output_path}")
        self.create_contact_sheet(frames, metadata, output_path)
        
        print(f"Contact sheet saved: {output_path}")
        return output_path


def main():
    """Command line interface for video contact sheet generator."""
    parser = argparse.ArgumentParser(
        description="Generate contact sheet thumbnails for videos with scene detection"
    )
    parser.add_argument("video", help="Path to input video file")
    parser.add_argument("-o", "--output", help="Output contact sheet path (default: auto-generated)")
    parser.add_argument("--max-frames", type=int, default=16, 
                       help="Maximum number of frames to extract (default: 16)")
    parser.add_argument("--cols", type=int, default=4,
                       help="Number of columns in contact sheet (default: 4)")
    parser.add_argument("--scene-thresh", type=float, default=0.3,
                       help="Scene change threshold 0.0-1.0 (default: 0.3)")
    parser.add_argument("--threads", type=int, default=4,
                       help="Number of processing threads (default: 4)")
    
    args = parser.parse_args()
    
    try:
        generator = VideoContactSheet(
            max_frames=args.max_frames,
            cols=args.cols,
            scene_thresh=args.scene_thresh,
            threads=args.threads
        )
        
        output_path = generator.generate_contact_sheet(args.video, args.output)
        print(f"\nSuccess! Contact sheet generated: {output_path}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()