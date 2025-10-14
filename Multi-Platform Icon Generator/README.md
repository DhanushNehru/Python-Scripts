# Multi-Platform Icon Generator

**Automates the tedious task of manually resizing a single logo/icon into 35+ different sizes required by modern app stores and platforms.**

## 📦 Dependencies

- **Pillow (PIL)** - Python Imaging Library for high-quality image processing

```bash
pip install Pillow
```

## How to Run

```bash
python icon_generator.py
```

## 📋 Available Options

1. **Generate all platform icons** - Creates icons for all platforms
2. **Generate specific platform** - Choose Android/iOS/Web/Windows/macOS
3. **Generate rounded icons only** - Modern rounded corner versions  
4. **Generate favicon.ico only** - Website favicon file
5. **Exit**

## 📸 Input

**Formats**: PNG, JPG, BMP, TIFF, GIF, WebP  
**Recommended**: PNG, 1024x1024px, square

## 📁 Output

```
your_image_icons/
├── android/     # 36px to 192px (6 sizes)
├── ios/         # 29px to 1024px (13 sizes)
├── web/         # 16px to 512px (5 sizes) 
├── windows/     # 16px to 256px (5 sizes)
├── macos/       # 16px to 1024px (6 sizes)
├── rounded/     # Various rounded sizes
├── favicon.ico
└── icon_preview.html
```