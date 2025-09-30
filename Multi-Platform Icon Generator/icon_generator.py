import subprocess
from pathlib import Path

def try_install_package(package_name):
    """Try to install a package using pip"""
    try:
        subprocess.check_call(["pip", "install", package_name], 
                            stdout=subprocess.DEVNULL, 
                            stderr=subprocess.DEVNULL)
        return True
    except:
        return False

# Standard icon sizes for different platforms
ICON_SIZES = {
    'android': [
        (36, 'ldpi'),
        (48, 'mdpi'),
        (72, 'hdpi'),
        (96, 'xhdpi'),
        (144, 'xxhdpi'),
        (192, 'xxxhdpi')
    ],
    'ios': [
        (20, 'iPhone-Notification'),
        (29, 'iPhone-Settings'),
        (40, 'iPhone-Spotlight'),
        (58, 'iPhone-Settings@2x'),
        (60, 'iPhone-App'),
        (76, 'iPad-App'),
        (80, 'iPhone-Spotlight@2x'),
        (87, 'iPhone-Settings@3x'),
        (120, 'iPhone-App@2x'),
        (152, 'iPad-App@2x'),
        (167, 'iPad-Pro'),
        (180, 'iPhone-App@3x'),
        (1024, 'App-Store')
    ],
    'web': [
        (16, 'favicon-16x16'),
        (32, 'favicon-32x32'),
        (96, 'favicon-96x96'),
        (192, 'android-chrome-192x192'),
        (512, 'android-chrome-512x512')
    ],
    'windows': [
        (16, 'small'),
        (32, 'medium'),
        (48, 'large'),
        (64, 'extra-large'),
        (256, 'jumbo')
    ],
    'macos': [
        (16, 'icon_16x16'),
        (32, 'icon_32x32'),
        (128, 'icon_128x128'),
        (256, 'icon_256x256'),
        (512, 'icon_512x512'),
        (1024, 'icon_1024x1024')
    ]
}

def generate_icons_with_pillow(input_image, output_dir, platform='all'):
    """Generate icons using Pillow (PIL)"""
    try:
        from PIL import Image
        
        # Open and validate input image
        with Image.open(input_image) as img:
            # Convert to RGBA for transparency support
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Get original size
            original_size = img.size
            print(f"Original image size: {original_size[0]}x{original_size[1]}")
            
            output_path = Path(output_dir)
            
            # To Determine which platforms to generate
            platforms_to_generate = [platform] if platform != 'all' else ICON_SIZES.keys()
            
            total_generated = 0
            
            for plat in platforms_to_generate:
                if plat not in ICON_SIZES:
                    continue
                
                # Create platform directory
                platform_dir = output_path / plat
                platform_dir.mkdir(parents=True, exist_ok=True)
                
                print(f"\n📱 Generating {plat.upper()} icons...")
                
                for size, name in ICON_SIZES[plat]:
                    try:
                        # Resize image with high quality
                        resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
                        
                        # Save icon
                        icon_path = platform_dir / f"{name}.png"
                        resized_img.save(icon_path, "PNG", optimize=True)
                        
                        print(f"  ✅ {size}x{size} - {icon_path.name}")
                        total_generated += 1
                        
                    except Exception as e:
                        print(f"  ❌ Failed to create {size}x{size}: {e}")
            
            return total_generated
            
    except ImportError:
        print("Installing Pillow...")
        if try_install_package("Pillow"):
            return generate_icons_with_pillow(input_image, output_dir, platform)
        return 0
    except Exception as e:
        print(f"❌ Error generating icons: {e}")
        return 0

def generate_rounded_icons(input_image, output_dir, corner_radius=0.2):
    """Generate rounded corner icons"""
    try:
        from PIL import Image, ImageDraw
        
        with Image.open(input_image) as img:
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            output_path = Path(output_dir) / "rounded"
            output_path.mkdir(parents=True, exist_ok=True)
            
            print(f"\n🔄 Generating rounded icons...")
            
            # Common sizes for rounded icons
            sizes = [48, 96, 144, 192, 256, 512]
            generated = 0
            
            for size in sizes:
                try:
                    # Resize image
                    resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
                    
                    # Create rounded mask
                    mask = Image.new('L', (size, size), 0)
                    draw = ImageDraw.Draw(mask)
                    
                    # To calculate corner radius
                    radius = int(size * corner_radius)
                    
                    # Rounded rectangle
                    draw.rounded_rectangle([(0, 0), (size-1, size-1)], radius=radius, fill=255)
                    
                    # Apply mask
                    rounded_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
                    rounded_img.paste(resized_img, (0, 0))
                    rounded_img.putalpha(mask)
                    
                    # Rounded icon
                    icon_path = output_path / f"rounded_icon_{size}x{size}.png"
                    rounded_img.save(icon_path, "PNG")
                    
                    print(f"  ✅ {size}x{size} rounded - {icon_path.name}")
                    generated += 1
                    
                except Exception as e:
                    print(f"  ❌ Failed to create rounded {size}x{size}: {e}")
            
            return generated
            
    except Exception as e:
        print(f"❌ Error generating rounded icons: {e}")
        return 0

def generate_favicon_ico(input_image, output_dir):
    """Generate Windows ICO format favicon"""
    try:
        from PIL import Image
        
        with Image.open(input_image) as img:
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            print(f"\n🌐 Generating favicon.ico...")
            
            # Create multiple sizes for ICO
            sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
            images = []
            
            for size in sizes:
                resized = img.resize(size, Image.Resampling.LANCZOS)
                images.append(resized)
            
            # Save as ICO
            ico_path = output_path / "favicon.ico"
            images[0].save(ico_path, format='ICO', sizes=sizes)
            
            print(f"  ✅ favicon.ico created - {ico_path.name}")
            return 1
            
    except Exception as e:
        print(f"❌ Error generating ICO: {e}")
        return 0

def create_icon_preview(output_dir):
    """Create HTML preview of generated icons"""
    try:
        output_path = Path(output_dir)
        
        html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Icon Preview</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .platform { margin: 20px 0; }
        .icon-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 20px; }
        .icon-item { text-align: center; padding: 10px; border: 1px solid #ddd; border-radius: 8px; }
        .icon-item img { max-width: 100px; max-height: 100px; }
        .icon-size { font-size: 12px; color: #666; margin-top: 5px; }
        h1 { color: #333; }
        h2 { color: #666; border-bottom: 2px solid #eee; padding-bottom: 5px; }
    </style>
</head>
<body>
    <h1>Generated Icons Preview</h1>
"""
        
        # Find all generated icons
        for platform_dir in output_path.iterdir():
            if platform_dir.is_dir():
                icons = list(platform_dir.glob("*.png"))
                if icons:
                    html_content += f"""
    <div class="platform">
        <h2>{platform_dir.name.upper()} Icons</h2>
        <div class="icon-grid">
"""
                    
                    for icon in sorted(icons):
                        try:
                            from PIL import Image
                            with Image.open(icon) as img:
                                size = img.size
                            
                            relative_path = icon.relative_to(output_path)
                            html_content += f"""
            <div class="icon-item">
                <img src="{relative_path}" alt="{icon.stem}">
                <div class="icon-size">{icon.stem}<br>{size[0]}x{size[1]}</div>
            </div>
"""
                        except:
                            pass
                    
                    html_content += """
        </div>
    </div>
"""
        
        html_content += """
</body>
</html>
"""
        
        # Save HTML preview
        preview_path = output_path / "icon_preview.html"
        preview_path.write_text(html_content, encoding='utf-8')
        
        print(f"\n📄 HTML preview created: {preview_path.name}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating preview: {e}")
        return False

def main():
    print("🎨 Icon Generator")
    print("Create app icons in multiple sizes for different platforms!")
    print("="*60)
    
    while True:
        print("\nChoose an option:")
        print("1. Generate icons from single image")
        print("2. Generate specific platform icons")
        print("3. Generate rounded icons only")
        print("4. Generate favicon.ico only")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == "1":
            input_image = input("\nEnter image file path: ").strip().strip('"')
            if input_image and Path(input_image).exists():
                output_dir = input("Enter output directory (or press Enter for auto): ").strip().strip('"')
                if not output_dir:
                    output_dir = Path(input_image).stem + "_icons"
                
                print(f"\n🎨 Generating icons from: {Path(input_image).name}")
                
                total = 0
                total += generate_icons_with_pillow(input_image, output_dir, 'all')
                total += generate_rounded_icons(input_image, output_dir)
                total += generate_favicon_ico(input_image, output_dir)
                
                if total > 0:
                    create_icon_preview(output_dir)
                    print(f"\n🎉 Generated {total} icons in: {output_dir}")
                
            else:
                print("❌ Invalid file path")
                
        elif choice == "2":
            input_image = input("\nEnter image file path: ").strip().strip('"')
            if input_image and Path(input_image).exists():
                print("\nAvailable platforms:")
                for i, platform in enumerate(ICON_SIZES.keys(), 1):
                    print(f"{i}. {platform}")
                
                platform_choice = input("\nEnter platform number: ").strip()
                try:
                    platform_idx = int(platform_choice) - 1
                    platform = list(ICON_SIZES.keys())[platform_idx]
                    
                    output_dir = input("Enter output directory (or press Enter for auto): ").strip().strip('"')
                    if not output_dir:
                        output_dir = f"{Path(input_image).stem}_{platform}_icons"
                    
                    generated = generate_icons_with_pillow(input_image, output_dir, platform)
                    
                    if generated > 0:
                        create_icon_preview(output_dir)
                        print(f"\n🎉 Generated {generated} {platform} icons")
                        
                except (ValueError, IndexError):
                    print("❌ Invalid platform choice")
            else:
                print("❌ Invalid file path")
                
        elif choice == "3":
            input_image = input("\nEnter image file path: ").strip().strip('"')
            if input_image and Path(input_image).exists():
                output_dir = input("Enter output directory (or press Enter for auto): ").strip().strip('"')
                if not output_dir:
                    output_dir = Path(input_image).stem + "_rounded_icons"
                
                corner_radius = input("Enter corner radius (0.1-0.5, default 0.2): ").strip()
                try:
                    corner_radius = float(corner_radius) if corner_radius else 0.2
                except ValueError:
                    corner_radius = 0.2
                
                generated = generate_rounded_icons(input_image, output_dir, corner_radius)
                
                if generated > 0:
                    create_icon_preview(output_dir)
                    print(f"\n🎉 Generated {generated} rounded icons")
            else:
                print("❌ Invalid file path")
                
        elif choice == "4":
            input_image = input("\nEnter image file path: ").strip().strip('"')
            if input_image and Path(input_image).exists():
                output_dir = input("Enter output directory (or press Enter for auto): ").strip().strip('"')
                if not output_dir:
                    output_dir = Path(input_image).parent
                
                generated = generate_favicon_ico(input_image, output_dir)
                
                if generated > 0:
                    print(f"\n🎉 Generated favicon.ico")
            else:
                print("❌ Invalid file path")
                
        elif choice == "5":
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice, please try again")

if __name__ == "__main__":
    main()