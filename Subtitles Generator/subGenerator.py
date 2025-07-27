import os
import whisper
from whisper.utils import get_writer
import ffmpeg

class SubtitleGenerator:
    def __init__(self, model_size):
        """
        Initialize the subtitle generator with a Whisper model
        
        Args:
            model_size (str): Size of the Whisper model (medium or large)
        """
        self.model = whisper.load_model(model_size)
        self.supported_languages = set(whisper.tokenizer.LANGUAGES.values())
    
    @staticmethod
    def extract_audio(video_path, audio_path):
        """
        Extract audio from video file using ffmpeg
        
        Args:
            video_path (str): Path to the video file
            audio_path (str): Path to save the extracted audio
        """
        stream = ffmpeg.input(video_path)
        stream = ffmpeg.output(stream, audio_path, ac=1, ar=16000)
        stream = ffmpeg.overwrite_output(stream)
        stream.run(quiet=True)
        return audio_path
    
    def transcribe(self, audio_path, language=None):
        """
        Transcribe audio file to text with timestamps, raise an error
        if the language is not available
        
        Args:
            audio_path (str): Path to the audio file
        """
        if language is not None and language not in self.supported_languages:
            raise ValueError(f"Language {language} not available.")
        return self.model.transcribe(audio_path, word_timestamps=True, language=language)
    
    @staticmethod
    def generate_srt(result, output_path):
        """
        Generate SRT file from transcription result
    
        Args:
            result (dict): Transcription result from Whisper
            output_path (str): Path to save the SRT file
        """
        srt_writer = get_writer("srt", os.path.dirname(output_path))
        srt_writer(result, output_path)
    
    def process_file(self, input_path, output_path=None):
        """
        Process input file and generate a SRT file
        
        Args:
            input_path (str): Path to input audio/video file
            output_path (str): Path to output SRT file (optional)
        """
        if output_path is None:
            base_name = os.path.splitext(input_path)[0]
            output_path = f"{base_name}.srt"
        
        is_video = input_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))
        
        audio_path = input_path
        if is_video:
            print("Extracting audio from video...")
            audio_path = "temp_audio.wav"
            self.extract_audio(input_path, audio_path)
        try: 
            print("Transcribing audio...")
            result = self.transcribe(audio_path)
                
            print("Generating subtitles...")
            self.generate_srt(result, output_path)
                
            print(f"Subtitles generated successfully: {output_path}")
        finally:       
            if is_video:
                os.remove(audio_path)

    @staticmethod
    def mux_subtitles(video_path, subtitle_paths, output_path=None):
        """
        Combine a video with one or more SRT files

        Args:
            video_path (str): Path to input video file
            subtitle_paths (list of str): List of paths to input SRT files
            output_path (str): Path to output mkv or mp4 file (optional)
        """
        print(f"Generating .mkv file with soft subtitles")

        if output_path is None:
            base_name = os.path.splitext(video_path)[0]
            output_path = f"{base_name}_subtitled.mkv"

        output_ext = os.path.splitext(output_path)[1].lower()
        if output_ext == '.mp4' and len(subtitle_paths) > 1:
            print("Warning: .mp4 only allow one subtitle. The first one will be used.")
            subtitle_paths = [subtitle_paths[0]]

        video_input = ffmpeg.input(video_path)
        video_stream = video_input.video
        audio_stream = video_input.audio

        if output_ext == '.mp4':
            subtitle_input = ffmpeg.input(subtitle_paths[0])
            output_kwargs = {'c:v': 'copy', 'c:a': 'copy', 'c:s': 'mov_text'}
            output_stream = ffmpeg.output(video_stream, audio_stream, subtitle_input, output_path, **output_kwargs)
        else:
            subtitle_inputs = [ffmpeg.input(s) for s in subtitle_paths]
            output_kwargs = {'c:v': 'copy', 'c:a': 'copy', 'c:s': 'srt'}
            output_stream = ffmpeg.output(video_stream, audio_stream, *subtitle_inputs, output_path, **output_kwargs)

        ffmpeg.run(output_stream, overwrite_output=True, quiet=True)
        print(f"File generated successfully: {output_path}")