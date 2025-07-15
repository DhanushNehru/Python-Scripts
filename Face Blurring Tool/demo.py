#!/usr/bin/env python3
"""
Face Blur Demo
==============

Simple demonstration of the face blurring tool.
Run this to test the functionality quickly!
"""

import cv2
import numpy as np
import os

def get_demo_image():
    """Get a demo image from user input or create a simple one."""
    print("📸 Choose your demo option:")
    print("1. Use your own image (recommended)")
    print("2. Use webcam to capture a photo")
    print("3. Create a simple test pattern")
    
    try:
        choice = input("Enter choice (1/2/3): ").strip()
        
        if choice == "1":
            # User provides image
            image_path = input("Enter path to your image: ").strip().strip('"')
            if os.path.exists(image_path):
                img = cv2.imread(image_path)
                if img is not None:
                    # Copy to demo location
                    cv2.imwrite("demo_face.jpg", img)
                    print(f"✔️ Using your image: {image_path}")
                    return True
                else:
                    print("✖️ Could not read the image file")
            else:
                print("✖️ File not found")
                
        elif choice == "2":
            # Capture from webcam
            return capture_from_webcam()
            
        elif choice == "3":
            # Create test pattern
            return create_test_pattern()
            
    except KeyboardInterrupt:
        print("\n Demo cancelled by user")
        return False
    
    # Fallback to test pattern
    print("⚠️ Falling back to test pattern...")
    return create_test_pattern()

def capture_from_webcam():
    """Capture a photo from webcam for demo."""
    try:
        print("📷 Opening webcam... Press SPACE to capture, ESC to cancel")
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("✖️ Could not open webcam")
            return False
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("✖️ Failed to read from webcam")
                break
                
            # Show preview
            cv2.putText(frame, "Press SPACE to capture, ESC to cancel", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow('Webcam - Demo Capture', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == 32:  # SPACE key
                cv2.imwrite("demo_face.jpg", frame)
                print("Photo captured for demo!")
                cap.release()
                cv2.destroyAllWindows()
                return True
            elif key == 27:  # ESC key
                break
        
        cap.release()
        cv2.destroyAllWindows()
        return False
        
    except Exception as e:
        print(f"✖️ Webcam capture failed: {e}")
        return False

def create_test_pattern():
    """Create a simple test pattern as fallback."""
    print("Creating test pattern...")
    img = np.ones((400, 600, 3), dtype=np.uint8) * 240
    
    # Draw a simple face that's more likely to be detected
    center = (300, 200)
    
    # Face oval
    cv2.ellipse(img, center, (80, 100), 0, 0, 360, (200, 180, 160), -1)
    
    # Eyes (larger and more prominent)
    cv2.ellipse(img, (270, 180), (15, 8), 0, 0, 360, (50, 50, 50), -1)
    cv2.ellipse(img, (330, 180), (15, 8), 0, 0, 360, (50, 50, 50), -1)
    
    # Eye pupils
    cv2.circle(img, (270, 180), 5, (0, 0, 0), -1)
    cv2.circle(img, (330, 180), 5, (0, 0, 0), -1)
    
    # Nose
    points = np.array([[300, 200], [295, 215], [305, 215]], np.int32)
    cv2.fillPoly(img, [points], (150, 120, 100))
    
    # Mouth
    cv2.ellipse(img, (300, 240), (20, 10), 0, 0, 180, (100, 50, 50), 3)
    
    # Hair
    cv2.ellipse(img, (300, 120), (90, 40), 0, 0, 180, (100, 80, 60), -1)
    
    cv2.imwrite("demo_face.jpg", img)
    print("Test pattern created")
    return True

def quick_demo():
    """Run a quick demo of the face blurring tool."""
    print("Face Blur Tool - Quick Demo")
    print("=" * 35)
    
    # Get demo image from user
    if not get_demo_image():
        print("✖️ Could not get demo image. Exiting...")
        return
    
    # Try to import and use the main tool
    try:
        from face_blur import FaceBlurrer
        
        # Test with different methods
        methods = ['haar', 'mediapipe']
        
        print("\n Testing face detection methods...")
        
        for method in methods:
            try:
                print(f"   Testing {method}...")
                blurrer = FaceBlurrer(method=method, blur_type='gaussian', blur_intensity=25)
                success = blurrer.process_image("demo_face.jpg", f"demo_blurred_{method}.jpg")
                
                if success:
                    print(f" {method} method worked!")
                else:
                    print(f" ⚠️  {method} method had issues")

            except Exception as e:
                print(f"✖️ {method} method failed: {e}")
        
        print(f"\n🎉 Demo completed! Check the generated images.")
        
        # Ask about webcam test
        try:
            response = input("\n📹 Want to test with webcam? (y/n): ").lower()
            if response == 'y':
                print("🚀 Starting webcam demo... Press 'q' to quit!")
                blurrer = FaceBlurrer(method='haar', blur_type='gaussian', blur_intensity=21)
                blurrer.process_webcam()
        except KeyboardInterrupt:
            print("\n Demo stopped by user")
            
    except ImportError as e:
        print(f"✖️ Could not import face_blur module: {e}")
        print(" Make sure face_blur.py is in the same directory!")

def main():
    """Main demo function."""
    quick_demo()

if __name__ == "__main__":
    main()
