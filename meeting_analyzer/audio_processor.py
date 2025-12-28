"""
Audio processor module for extracting and transcribing audio from video files
"""

import os
import subprocess
from pathlib import Path
from typing import Optional
import json


class AudioProcessor:
    """Processes audio from video files and performs transcription"""
    
    def __init__(self, video_path: str, output_dir: str = "output/audio"):
        """
        Initialize the audio processor
        
        Args:
            video_path: Path to the video file
            output_dir: Directory to save extracted audio
        """
        self.video_path = video_path
        self.output_dir = output_dir
        self.audio_path = None
        
        os.makedirs(output_dir, exist_ok=True)
    
    def extract_audio(self, audio_format: str = "wav") -> str:
        """
        Extract audio from video file
        
        Args:
            audio_format: Output audio format (wav, mp3)
            
        Returns:
            Path to extracted audio file
        """
        video_name = Path(self.video_path).stem
        audio_path = os.path.join(self.output_dir, f"{video_name}.{audio_format}")
        
        print(f"Extracting audio from video...")
        
        try:
            # Use ffmpeg to extract audio
            cmd = [
                "ffmpeg", "-y", "-i", self.video_path,
                "-vn", "-acodec", "pcm_s16le" if audio_format == "wav" else "libmp3lame",
                "-ar", "16000",  # 16kHz sample rate for speech
                "-ac", "1",  # Mono
                audio_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            print(f"Audio extracted to: {audio_path}")
            self.audio_path = audio_path
            return audio_path
            
        except subprocess.CalledProcessError as e:
            # Audio extraction failed - ffmpeg may not be installed or video may not have audio
            print("Audio extraction failed. Ensure ffmpeg is installed.")
            if e.stderr:
                print(f"Error details: {e.stderr}")
            print("Note: Install ffmpeg for audio extraction support")
            return None
        except FileNotFoundError:
            print("ffmpeg not found in PATH")
            print("Note: Install ffmpeg for audio extraction support")
            return None
    
    def transcribe_audio_local(self, model: str = "small", device: str = "auto") -> dict:
        """
        Transcribe audio using local faster-whisper
        
        Args:
            model: Whisper model size (tiny, base, small, medium, large)
            device: Device to use ("auto", "cuda", "cpu")
            
        Returns:
            Dictionary with transcription results
        """
        if not self.audio_path:
            raise ValueError("No audio file available. Extract audio first.")
        
        try:
            from faster_whisper import WhisperModel
            
            print(f"Transcribing audio using local Whisper ({model} model)...")
            
            # Auto-detect device if set to "auto"
            if device == "auto":
                try:
                    import torch
                    device = "cuda" if torch.cuda.is_available() else "cpu"
                except ImportError:
                    device = "cpu"
            
            compute_type = "float16" if device == "cuda" else "int8"
            print(f"  Using device: {device} (compute type: {compute_type})")
            
            # Initialize model
            model_instance = WhisperModel(model, device=device, compute_type=compute_type)
            
            # Transcribe
            segments, info = model_instance.transcribe(
                self.audio_path,
                beam_size=5,
                vad_filter=True,  # Voice activity detection
                vad_parameters=dict(min_silence_duration_ms=500)
            )
            
            # Collect segments
            segment_list = []
            full_text = []
            
            for segment in segments:
                segment_data = {
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text
                }
                segment_list.append(segment_data)
                full_text.append(segment.text)
            
            result = {
                "text": " ".join(full_text),
                "language": info.language,
                "duration": info.duration,
                "segments": segment_list
            }
            
            print(f"Transcription complete. Length: {len(result['text'])} characters")
            print(f"  Detected language: {info.language}")
            print(f"  Duration: {info.duration:.2f}s")
            
            # Save transcription to file
            transcript_path = os.path.join(
                self.output_dir,
                f"{Path(self.audio_path).stem}_transcript.json"
            )
            with open(transcript_path, 'w') as f:
                json.dump(result, f, indent=2)
            
            print(f"Transcription saved to: {transcript_path}")
            
            return result
            
        except ImportError:
            raise ImportError("faster-whisper not installed. Install with: pip install faster-whisper")
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")
    
    def transcribe_audio_openai(self, api_key: str, model: str = "whisper-1") -> dict:
        """
        Transcribe audio using OpenAI Whisper API (backward compatibility)
        
        Args:
            api_key: OpenAI API key
            model: Whisper model to use
            
        Returns:
            Dictionary with transcription results
        """
        if not self.audio_path:
            raise ValueError("No audio file available. Extract audio first.")
        
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=api_key)
            
            print(f"Transcribing audio using OpenAI Whisper ({model})...")
            
            with open(self.audio_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model=model,
                    file=audio_file,
                    response_format="verbose_json"
                )
            
            result = {
                "text": transcript.text,
                "language": getattr(transcript, 'language', 'en'),
                "duration": getattr(transcript, 'duration', None),
                "segments": getattr(transcript, 'segments', [])
            }
            
            print(f"Transcription complete. Length: {len(result['text'])} characters")
            
            # Save transcription to file
            transcript_path = os.path.join(
                self.output_dir,
                f"{Path(self.audio_path).stem}_transcript.json"
            )
            with open(transcript_path, 'w') as f:
                json.dump(result, f, indent=2)
            
            print(f"Transcription saved to: {transcript_path}")
            
            return result
            
        except ImportError:
            raise ImportError("OpenAI library not installed. Install with: pip install openai")
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")
    
    def get_audio_metadata(self) -> dict:
        """
        Get audio metadata
        
        Returns:
            Dictionary with audio metadata
        """
        if not self.audio_path or not os.path.exists(self.audio_path):
            return {"status": "no_audio_file"}
        
        # Basic metadata
        metadata = {
            "path": self.audio_path,
            "size_bytes": os.path.getsize(self.audio_path),
            "format": Path(self.audio_path).suffix[1:]
        }
        
        return metadata
