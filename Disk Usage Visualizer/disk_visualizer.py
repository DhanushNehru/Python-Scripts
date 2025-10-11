import os

def get_dir_sizes(path="."):
    dir_sizes = {}
    for root, dirs, files in os.walk(path):
        for name in files:
            try:
                full_path = os.path.join(root, name)

                # Handle long paths in Windows
                if os.name == "nt":
                    full_path = r"\\?\\" + os.path.abspath(full_path)

                size = os.path.getsize(full_path)
                dir_path = os.path.relpath(root, path)
                dir_sizes[dir_path] = dir_sizes.get(dir_path, 0) + size
            except (FileNotFoundError, PermissionError, OSError):
                continue
    return dir_sizes


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Disk Usage Visualizer (CLI)")
    parser.add_argument("path", nargs="?", default=".", help="Path to analyze")
    parser.add_argument(
        "-n", "--top", type=int, default=10, help="Show top N largest directories"
    )
    args = parser.parse_args()

    print(f"Analyzing disk usage in: {args.path}\n")

    dir_sizes = get_dir_sizes(args.path)

    # Sort by size (descending)
    sorted_dirs = sorted(dir_sizes.items(), key=lambda x: x[1], reverse=True)

    print(f"Top {args.top} largest directories:")
    print("-" * 60)
    print(f"{'Directory':40s} | {'Size (MB)':>10s}")
    print("-" * 60)

    for dir_path, size in sorted_dirs[: args.top]:
        size_mb = size / (1024 * 1024)
        print(f"{dir_path:40s} | {size_mb:10.2f}")

    print("-" * 60)
    print("✅ Disk usage analysis complete.")


if __name__ == "__main__":
    main()
