"""
Main meeting analyzer orchestrator
"""

import os
from pathlib import Path
from typing import Optional
import json

from .video_processor import VideoProcessor
from .audio_processor import AudioProcessor
from .ai_analyzer import AIAnalyzer
from .srs_generator import SRSGenerator


class MeetingAnalyzer:
    """Main orchestrator for meeting analysis"""
    
    def __init__(self, 
                 video_path: str,
                 lm_studio_url: str = "http://localhost:1234/v1",
                 text_model: str = "phi-3-mini",
                 vision_model: str = "llava-7b-q4",
                 whisper_model: str = "small",
                 vision_on_cpu: bool = False,
                 output_dir: str = "output",
                 openai_api_key: Optional[str] = None,
                 openai_model: Optional[str] = None,
                 openai_whisper_model: Optional[str] = None):
        """
        Initialize the meeting analyzer
        
        Args:
            video_path: Path to the meeting video file
            lm_studio_url: LM Studio base URL (default: http://localhost:1234/v1)
            text_model: Text model name for LM Studio (default: phi-3-mini)
            vision_model: Vision model name for LM Studio (default: llava-7b-q4)
            whisper_model: Local Whisper model size (default: small)
            vision_on_cpu: Whether to run vision model on CPU (default: False)
            output_dir: Directory for output files
            openai_api_key: OpenAI API key (optional, for backward compatibility)
            openai_model: OpenAI model to use (optional, for backward compatibility)
            openai_whisper_model: OpenAI Whisper model (optional, for backward compatibility)
        """
        self.video_path = video_path
        self.lm_studio_url = lm_studio_url
        self.text_model = text_model
        self.vision_model = vision_model
        self.whisper_model = whisper_model
        self.vision_on_cpu = vision_on_cpu
        self.output_dir = output_dir
        self.openai_api_key = openai_api_key
        self.openai_model = openai_model
        self.openai_whisper_model = openai_whisper_model
        
        # Create output directories
        os.makedirs(output_dir, exist_ok=True)
        self.frames_dir = os.path.join(output_dir, "frames")
        self.audio_dir = os.path.join(output_dir, "audio")
        
        # Initialize processors
        self.video_processor = VideoProcessor(video_path, self.frames_dir)
        self.audio_processor = AudioProcessor(video_path, self.audio_dir)
        self.ai_analyzer = AIAnalyzer(lm_studio_url, text_model, vision_model, vision_on_cpu)
        self.srs_generator = SRSGenerator(output_dir)
        
        self.results = {}
    
    def analyze(self, 
                extract_frames_interval: int = 10,
                extract_key_frames: bool = True,
                max_key_frames: int = 15,
                max_frames_to_analyze: int = 10,
                project_name: str = "Meeting Project") -> dict:
        """
        Run the complete analysis pipeline
        
        Args:
            extract_frames_interval: Interval in seconds for frame extraction
            extract_key_frames: Whether to extract key frames based on scene changes
            max_key_frames: Maximum number of key frames to extract
            max_frames_to_analyze: Maximum number of frames to send to AI for analysis
            project_name: Name of the project for SRS document
            
        Returns:
            Dictionary with analysis results
        """
        print("=" * 60)
        print("MEETING ANALYZER - Starting Analysis")
        print("=" * 60)
        print(f"Video: {self.video_path}")
        print(f"Output Directory: {self.output_dir}")
        print()
        
        # Step 1: Extract video frames
        print("Step 1: Extracting video frames...")
        print("-" * 60)
        try:
            if extract_key_frames:
                frame_paths = self.video_processor.extract_key_frames(
                    threshold=30.0,
                    max_frames=max_key_frames
                )
            else:
                frame_paths = self.video_processor.extract_frames(
                    interval_seconds=extract_frames_interval
                )
            
            video_metadata = self.video_processor.get_video_metadata()
            self.results['video_metadata'] = video_metadata
            self.results['frame_paths'] = frame_paths
            print(f"✓ Extracted {len(frame_paths)} frames")
            print()
        except Exception as e:
            print(f"✗ Error extracting frames: {str(e)}")
            self.results['frame_paths'] = []
        
        # Step 2: Extract and transcribe audio
        print("Step 2: Extracting and transcribing audio...")
        print("-" * 60)
        try:
            audio_path = self.audio_processor.extract_audio()
            
            if audio_path:
                # Use local whisper by default, fallback to OpenAI if configured
                if self.openai_api_key and self.openai_whisper_model:
                    print("Using OpenAI Whisper (backward compatibility mode)")
                    transcription = self.audio_processor.transcribe_audio_openai(
                        self.openai_api_key,
                        self.openai_whisper_model
                    )
                else:
                    transcription = self.audio_processor.transcribe_audio_local(
                        self.whisper_model
                    )
                self.results['transcription'] = transcription
                print(f"✓ Transcription complete: {len(transcription['text'])} characters")
            else:
                print("⚠ Audio extraction skipped (ffmpeg not available)")
                self.results['transcription'] = {
                    'text': 'Audio transcription not available. Install ffmpeg for audio support.',
                    'status': 'skipped'
                }
            print()
        except Exception as e:
            print(f"✗ Error processing audio: {str(e)}")
            self.results['transcription'] = {
                'text': f'Error: {str(e)}',
                'status': 'error'
            }
        
        # Step 3: Analyze frames with AI
        print("Step 3: Analyzing visual content with AI...")
        print("-" * 60)
        try:
            if frame_paths:
                # Limit frames for efficiency
                frames_to_analyze = frame_paths[:max_frames_to_analyze]
                if len(frame_paths) > max_frames_to_analyze:
                    print(f"Note: Analyzing {max_frames_to_analyze} of {len(frame_paths)} frames")
                frame_analyses = self.ai_analyzer.analyze_frames(frames_to_analyze)
                self.results['frame_analyses'] = frame_analyses
                print(f"✓ Analyzed {len(frame_analyses)} frames")
            else:
                print("⚠ No frames to analyze")
                self.results['frame_analyses'] = []
            print()
        except Exception as e:
            print(f"✗ Error analyzing frames: {str(e)}")
            self.results['frame_analyses'] = []
        
        # Step 4: Generate requirements
        print("Step 4: Generating requirements...")
        print("-" * 60)
        try:
            requirements = self.ai_analyzer.generate_requirements(
                self.results.get('transcription', {}),
                self.results.get('frame_analyses', [])
            )
            self.results['requirements'] = requirements
            print("✓ Requirements generated")
            print()
        except Exception as e:
            print(f"✗ Error generating requirements: {str(e)}")
            self.results['requirements'] = {'error': str(e)}
        
        # Step 5: Generate SRS documents
        print("Step 5: Generating SRS documents...")
        print("-" * 60)
        try:
            markdown_path = self.srs_generator.generate_markdown(
                self.results.get('requirements', {}),
                project_name
            )
            self.results['srs_markdown'] = markdown_path
            print(f"✓ Markdown SRS: {markdown_path}")
            
            docx_path = self.srs_generator.generate_docx(
                self.results.get('requirements', {}),
                project_name
            )
            if docx_path:
                self.results['srs_docx'] = docx_path
                print(f"✓ DOCX SRS: {docx_path}")
            
            json_path = self.srs_generator.save_json(
                self.results.get('requirements', {}),
                project_name
            )
            self.results['requirements_json'] = json_path
            print(f"✓ Requirements JSON: {json_path}")
            print()
        except Exception as e:
            print(f"✗ Error generating SRS: {str(e)}")
        
        # Save complete results
        results_path = os.path.join(self.output_dir, "analysis_results.json")
        with open(results_path, 'w', encoding='utf-8') as f:
            # Create serializable version of results
            serializable_results = {
                k: v for k, v in self.results.items() 
                if k not in ['frame_paths']  # Exclude large data
            }
            serializable_results['frame_count'] = len(self.results.get('frame_paths', []))
            json.dump(serializable_results, f, indent=2)
        
        print("=" * 60)
        print("ANALYSIS COMPLETE")
        print("=" * 60)
        print(f"Results saved to: {results_path}")
        print()
        
        return self.results
