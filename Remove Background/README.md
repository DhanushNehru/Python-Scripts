# Background/Foreground Remover & Replacer

A modern Qt-based GUI application for advanced image processing that allows you to remove and replace backgrounds or foregrounds in images with various options including solid colors, images, and gradients.

## Features

### Core Functionality
- **Background Removal**: Remove backgrounds from images using adaptive thresholding and morphological operations
- **Background Replacement**: Replace backgrounds with solid colors, custom images, or gradients
- **Foreground Removal**: Remove foreground elements from images
- **Foreground Replacement**: Replace foregrounds with solid colors, custom images, or gradients

### Replacement Options
Both background and foreground operations support three replacement types:

1. **Solid Color**: Choose any custom color using an interactive color picker
2. **Image**: Load a custom image file (JPG, PNG, BMP) to use as replacement
3. **Gradient**: Create custom gradients with two color stops using color pickers

### User Interface
- **Modern Dark Theme**: Clean, professional dark interface using Qt Fusion style
- **Real-time Preview**: View original and processed images side-by-side
- **Interactive Controls**: Tabbed interface for easy access to all replacement options
- **Progress Feedback**: Visual progress indication during image processing
- **Error Handling**: Comprehensive error messages and validation

## Requirements

```
PySide6>=6.0.0
opencv-python>=4.5.0
numpy>=1.20.0
```

## Installation

1. Install the required dependencies:
```bash
pip install PySide6 opencv-python numpy
```

2. Run the GUI application:
```bash
python bg_remover_gui.py
```

## Usage

### Basic Workflow

1. **Load Image**: Click "Load Image" to select an input image file
2. **Choose Operation**: Select from four operation modes:
   - Remove Background
   - Replace Background
   - Remove Foreground
   - Replace Foreground
3. **Configure Replacement** (for replace operations):
   - Navigate to the appropriate tab (Background/Foreground)
   - Choose replacement type (Color/Image/Gradient)
   - Configure settings using color pickers or image selection
4. **Process**: Click "Process Image" to apply the operation
5. **Save**: Click "Save Result" to export the processed image

### Operation Details

#### Remove Background/Foreground
Removes the specified portion of the image using:
- Color space conversion (BGR to GRAY)
- Adaptive binary thresholding
- Morphological operations (erosion, dilation)
- Gaussian blur for edge smoothing
- Alpha channel creation for transparency

#### Replace Background
Replaces the background while preserving the foreground:
- **Solid Color**: Select a single color to use as the new background
- **Image**: Load an image file that will be scaled to fit the background area
- **Gradient**: Create a vertical gradient with two colors (top and bottom)

#### Replace Foreground
Replaces the foreground while preserving the background:
- **Solid Color**: Select a single color to use as the new foreground
- **Image**: Load an image file that will be scaled to fit the foreground area
- **Gradient**: Create a vertical gradient with two colors (top and bottom)

### Tips for Best Results

- **Image Quality**: Use high-resolution images for better processing results
- **Subject Contrast**: Images with clear contrast between subject and background work best
- **Color Selection**: Use the color picker to precisely match or complement your image colors
- **Gradient Direction**: Gradients are currently vertical (top to bottom) for consistent results
- **Image Replacement**: Replacement images are automatically scaled to fit - use high-quality images

## Technical Details

### Image Processing Pipeline

1. **Input Validation**: Checks for valid image file and operation mode
2. **Color Space Conversion**: Converts BGR to GRAY for threshold operations
3. **Thresholding**: Applies binary threshold (127) with THRESH_BINARY_INV
4. **Morphological Operations**: 
   - Erosion with 5x5 kernel (2 iterations)
   - Dilation with 5x5 kernel (2 iterations)
5. **Edge Smoothing**: Gaussian blur (5x5 kernel) for natural boundaries
6. **Alpha Blending**: Combines processed mask with replacement content
7. **Output**: Returns BGRA image with alpha channel for transparency

### Architecture

- **ImageProcessor (QThread)**: Background thread for non-blocking image processing
  - Signals: `finished`, `error`, `progress`
  - Operations: `remove_bg`, `replace_bg`, `remove_fg`, `replace_fg`
  
- **BackgroundRemoverGUI (QMainWindow)**: Main application window
  - Image display with aspect ratio preservation
  - Tabbed interface for background and foreground controls
  - Color pickers with live preview
  - File selection dialogs
  - Progress indication

### Type Safety

The application uses strict type checking with:
- `cv2.typing.MatLike` for OpenCV matrices
- `Optional` types for nullable values
- `Dict[str, Any]` for configuration parameters
- Full type annotations throughout

## File Structure

```
Remove Background/
├── bg_remover_gui.py    # Main GUI application with Qt interface
├── code.py              # Simple command-line version (legacy)
├── README.md            # This documentation
└── requirements.txt     # Python dependencies (if present)
```

## Troubleshooting

### Common Issues

**Image not loading**
- Ensure the image file exists and is a valid format (JPG, PNG, BMP)
- Check file permissions

**Processing fails**
- Verify the image is not corrupted
- Try a different image to isolate the issue
- Check that all dependencies are installed correctly

**Replacement image doesn't look right**
- Use high-resolution replacement images
- Ensure replacement images are the same aspect ratio as the original
- Try adjusting the gradient colors or solid color selection

**GUI doesn't start**
- Verify PySide6 is installed: `pip install PySide6`
- Check for Qt conflicts if multiple Qt versions are installed
- Run from command line to see error messages

### Performance Notes

- Processing time varies based on image size and complexity
- Large images (>4K) may take several seconds to process
- Background operations run in a separate thread to keep UI responsive
- Each operation has a 30-second timeout to prevent hanging

## License

This project is part of the Python-Scripts repository. Please refer to the repository's LICENSE file for licensing information.

## Contributing

Contributions are welcome! Please follow the repository's contribution guidelines:
1. Fork the repository
2. Create a feature branch
3. Make your changes with proper type annotations
4. Test thoroughly with various image types
5. Submit a pull request

## Legacy Version

The `code.py` file contains a simpler command-line version of the background remover. This version:
- Takes input from command-line arguments
- Only supports basic background removal
- Saves output automatically
- Does not include replacement features

Use `bg_remover_gui.py` for the full-featured GUI experience.

## Future Enhancements

Potential improvements for future versions:
- Horizontal/diagonal gradient options
- Custom gradient with multiple color stops
- Batch processing for multiple images
- Additional morphological operations
- Machine learning-based segmentation
- Real-time video processing
- Custom threshold adjustment controls
- Edge detection algorithms selection
- Undo/redo functionality
- Image filters and adjustments

## Credits

Built with:
- **PySide6**: Qt6 bindings for Python
- **OpenCV**: Computer vision and image processing
- **NumPy**: Numerical computing for array operations
