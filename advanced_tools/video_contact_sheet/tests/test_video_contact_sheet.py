#!/usr/bin/env python3
"""
Tests for video contact sheet generator.
"""

import unittest
import tempfile
import os
import cv2
import numpy as np
import sys
from unittest.mock import patch

# Add parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from video_contact_sheet import VideoContactSheet


class TestVideoContactSheet(unittest.TestCase):
    """Test cases for VideoContactSheet class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.contact_sheet = VideoContactSheet(max_frames=8, cols=4, scene_thresh=0.3)
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def create_test_video(self, filename, duration_seconds=5, fps=30, width=640, height=480):
        """
        Create a test video with different colored scenes.
        
        Args:
            filename (str): Output video filename
            duration_seconds (int): Video duration in seconds
            fps (int): Frames per second
            width (int): Video width
            height (int): Video height
        
        Returns:
            str: Path to created video file
        """
        video_path = os.path.join(self.temp_dir, filename)
        
        # Define codec and create VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
        
        total_frames = duration_seconds * fps
        frames_per_scene = total_frames // 3  # 3 distinct scenes
        
        for frame_num in range(total_frames):
            # Create different colored scenes
            if frame_num < frames_per_scene:
                # Red scene
                frame = np.full((height, width, 3), (0, 0, 255), dtype=np.uint8)
            elif frame_num < 2 * frames_per_scene:
                # Green scene
                frame = np.full((height, width, 3), (0, 255, 0), dtype=np.uint8)
            else:
                # Blue scene
                frame = np.full((height, width, 3), (255, 0, 0), dtype=np.uint8)
            
            # Add some noise to make it more realistic
            noise = np.random.randint(0, 30, frame.shape, dtype=np.uint8)
            frame = cv2.add(frame, noise)
            
            out.write(frame)
        
        out.release()
        return video_path
    
    def test_video_creation(self):
        """Test that we can create a test video."""
        video_path = self.create_test_video("test_video.mp4")
        self.assertTrue(os.path.exists(video_path))
        
        # Verify video properties
        cap = cv2.VideoCapture(video_path)
        self.assertTrue(cap.isOpened())
        
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        self.assertGreater(frame_count, 0)
        self.assertGreater(fps, 0)
        
        cap.release()
    
    def test_scene_detection(self):
        """Test scene change detection functionality."""
        video_path = self.create_test_video("scene_test.mp4")
        
        frames = self.contact_sheet.detect_scene_changes(video_path)
        
        # Should detect multiple scenes
        self.assertGreater(len(frames), 1)
        self.assertLessEqual(len(frames), self.contact_sheet.max_frames)
        
        # Each frame should be a tuple of (frame_number, frame_image)
        for frame_data in frames:
            self.assertIsInstance(frame_data, tuple)
            self.assertEqual(len(frame_data), 2)
            frame_num, frame_img = frame_data
            self.assertIsInstance(frame_num, int)
            self.assertIsInstance(frame_img, np.ndarray)
    
    def test_histogram_calculation(self):
        """Test HSV histogram calculation."""
        # Create a simple test frame
        frame = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        
        hist = self.contact_sheet.calculate_histogram(frame)
        
        self.assertIsInstance(hist, np.ndarray)
        self.assertGreater(len(hist), 0)
    
    def test_video_metadata_extraction(self):
        """Test video metadata extraction."""
        video_path = self.create_test_video("metadata_test.mp4")
        
        metadata = self.contact_sheet.get_video_metadata(video_path)
        
        # Check required metadata fields
        required_fields = ['duration', 'resolution', 'codec', 'fps']
        for field in required_fields:
            self.assertIn(field, metadata)
        
        # Verify metadata values
        self.assertGreater(metadata['duration'], 0)
        self.assertIn('x', metadata['resolution'])
        self.assertGreater(metadata['fps'], 0)
    
    def test_contact_sheet_generation(self):
        """Test complete contact sheet generation."""
        video_path = self.create_test_video("full_test.mp4")
        output_path = os.path.join(self.temp_dir, "test_contact_sheet.jpg")
        
        result_path = self.contact_sheet.generate_contact_sheet(video_path, output_path)
        
        # Verify output file was created
        self.assertTrue(os.path.exists(result_path))
        self.assertEqual(result_path, output_path)
        
        # Verify it's a valid image file
        from PIL import Image
        with Image.open(result_path) as img:
            self.assertGreater(img.width, 0)
            self.assertGreater(img.height, 0)
            self.assertEqual(img.format, 'JPEG')
    
    def test_invalid_video_file(self):
        """Test handling of invalid video files."""
        invalid_path = os.path.join(self.temp_dir, "nonexistent.mp4")
        
        with self.assertRaises(FileNotFoundError):
            self.contact_sheet.generate_contact_sheet(invalid_path)
    
    def test_parameter_validation(self):
        """Test parameter validation."""
        # Test max_frames parameter
        generator = VideoContactSheet(max_frames=10)
        self.assertEqual(generator.max_frames, 10)
        
        # Test cols parameter
        generator = VideoContactSheet(cols=5)
        self.assertEqual(generator.cols, 5)
        
        # Test scene_thresh parameter
        generator = VideoContactSheet(scene_thresh=0.5)
        self.assertEqual(generator.scene_thresh, 0.5)
        
        # Test threads parameter
        generator = VideoContactSheet(threads=8)
        self.assertEqual(generator.threads, 8)
    
    def test_command_line_interface(self):
        """Test command line interface."""
        video_path = self.create_test_video("cli_test.mp4")
        output_path = os.path.join(self.temp_dir, "cli_output.jpg")
        
        # Mock command line arguments
        test_args = [
            'video_contact_sheet.py',
            video_path,
            '--output', output_path,
            '--max-frames', '6',
            '--cols', '3',
            '--scene-thresh', '0.4'
        ]
        
        from video_contact_sheet import main
        
        with patch('sys.argv', test_args):
            # Capture any exceptions
            try:
                main()
                # If no exception, verify output was created
                self.assertTrue(os.path.exists(output_path))
            except SystemExit as e:
                # main() calls sys.exit on success, which is expected
                self.assertEqual(e.code, None or 0)


class TestVideoContactSheetIntegration(unittest.TestCase):
    """Integration tests for the video contact sheet system."""
    
    def test_end_to_end_workflow(self):
        """Test the complete workflow from video to contact sheet."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a test video with distinct scenes
            video_path = os.path.join(temp_dir, "integration_test.mp4")
            
            # Create video with 4 distinct colored scenes
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(video_path, fourcc, 10, (320, 240))
            
            colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # Blue, Green, Red, Yellow
            frames_per_scene = 30
            
            for color_idx, color in enumerate(colors):
                for _ in range(frames_per_scene):
                    frame = np.full((240, 320, 3), color, dtype=np.uint8)
                    # Add frame number text to make frames unique
                    cv2.putText(frame, f"Scene {color_idx + 1}", (10, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    out.write(frame)
            
            out.release()
            
            # Generate contact sheet
            generator = VideoContactSheet(max_frames=8, cols=2, scene_thresh=0.3)
            output_path = os.path.join(temp_dir, "integration_output.jpg")
            
            result = generator.generate_contact_sheet(video_path, output_path)
            
            # Verify results
            self.assertTrue(os.path.exists(result))
            
            # Load and verify the contact sheet
            from PIL import Image
            with Image.open(result) as contact_sheet:
                # Should have reasonable dimensions
                self.assertGreater(contact_sheet.width, 200)
                self.assertGreater(contact_sheet.height, 200)
                
                # Should be in RGB mode
                self.assertEqual(contact_sheet.mode, 'RGB')


if __name__ == '__main__':
    unittest.main()