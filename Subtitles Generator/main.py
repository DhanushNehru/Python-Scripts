from subGenerator import SubtitleGenerator
import os

def main():
    input_path = "your file path" 
    subtitle_path = f"{os.path.splitext(input_path)[0]}.srt"  
    model = "medium / large"  
    mux = True  
    
    print(f"Processing: {input_path}")
    generator = SubtitleGenerator(model)
    generator.process_file(input_path, subtitle_path)

    if mux and input_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        generator.mux_subtitles(input_path, [subtitle_path], 'output path')

if __name__ == "__main__":
    main()
