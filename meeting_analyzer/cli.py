"""
Command-line interface for Meeting Analyzer
"""

import argparse
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from .analyzer import MeetingAnalyzer
from .profiles import get_profile, list_profiles, get_profile_description


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Meeting Analyzer - AI-powered tool to analyze meeting videos and generate SRS documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with local models (default)
  meeting-analyzer --video meeting.mp4
  
  # Use laptop profile (optimized for 4GB VRAM)
  meeting-analyzer --video meeting.mp4 --profile laptop
  
  # Use PC profile (optimized for 24GB VRAM)
  meeting-analyzer --video meeting.mp4 --profile pc
  
  # Use profile with custom override
  meeting-analyzer --video meeting.mp4 --profile laptop --whisper-model medium
  
  # Specify custom LM Studio URL
  meeting-analyzer --video meeting.mp4 --lm-studio-url http://localhost:1234/v1
  
  # Use different local Whisper model
  meeting-analyzer --video meeting.mp4 --whisper-model medium
  
  # Specify custom text and vision models
  meeting-analyzer --video meeting.mp4 --text-model llama-3.2-3b --vision-model llava-7b
  
  # Specify project name and output directory
  meeting-analyzer --video meeting.mp4 --project "My Project" --output ./results
  
  # Extract frames at 5-second intervals instead of key frames
  meeting-analyzer --video meeting.mp4 --interval 5 --no-key-frames
        """
    )
    
    # Required arguments
    parser.add_argument(
        "--video",
        required=True,
        help="Path to the meeting video file"
    )
    
    # Hardware profile
    parser.add_argument(
        "--profile",
        choices=["laptop", "pc", "custom"],
        help="Hardware profile: laptop (4GB VRAM), pc (24GB VRAM), or custom (manual settings)"
    )
    
    # LM Studio / Local AI options
    parser.add_argument(
        "--lm-studio-url",
        help="LM Studio base URL (default: http://localhost:1234/v1 or LM_STUDIO_URL env var)"
    )
    
    parser.add_argument(
        "--text-model",
        help="Text model name for LM Studio (default: phi-3-mini or LM_STUDIO_MODEL env var)"
    )
    
    parser.add_argument(
        "--vision-model",
        help="Vision model name for LM Studio (default: llava-7b-q4 or LM_STUDIO_VISION_MODEL env var)"
    )
    
    parser.add_argument(
        "--whisper-model",
        help="Local Whisper model size: tiny, base, small, medium, large (default: small or WHISPER_MODEL env var)"
    )
    
    # Output options
    parser.add_argument(
        "--project",
        default="Meeting Project",
        help="Project name for SRS document (default: Meeting Project)"
    )
    
    parser.add_argument(
        "--output",
        default="output",
        help="Output directory for generated files (default: ./output)"
    )
    
    # Frame extraction options
    parser.add_argument(
        "--interval",
        type=int,
        default=10,
        help="Frame extraction interval in seconds (default: 10)"
    )
    
    parser.add_argument(
        "--no-key-frames",
        action="store_true",
        help="Disable key frame extraction and use interval-based extraction"
    )
    
    parser.add_argument(
        "--max-frames",
        type=int,
        default=15,
        help="Maximum number of key frames to extract (default: 15)"
    )
    
    parser.add_argument(
        "--max-analyze",
        type=int,
        default=10,
        help="Maximum number of frames to analyze with AI (default: 10)"
    )
    
    # Backward compatibility: OpenAI options (optional)
    parser.add_argument(
        "--api-key",
        help="OpenAI API key (optional, for backward compatibility with OpenAI)"
    )
    
    parser.add_argument(
        "--model",
        help="OpenAI model to use (optional, for backward compatibility)"
    )
    
    parser.add_argument(
        "--openai-whisper-model",
        help="OpenAI Whisper model name to use instead of local (requires --api-key)"
    )
    
    args = parser.parse_args()
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Get profile from args or environment
    profile_name = args.profile or os.getenv("HARDWARE_PROFILE")
    
    # Load profile settings if specified
    profile_settings = {}
    if profile_name and profile_name != "custom":
        try:
            profile_settings = get_profile(profile_name)
            print(f"Using hardware profile: {profile_name}")
            print(f"  Description: {get_profile_description(profile_name)}")
        except ValueError as e:
            print(f"Warning: {str(e)}")
            print("Continuing with default/custom settings")
    
    # Get configuration from args or profile or environment variables
    # Priority: CLI args > profile settings > environment variables > defaults
    lm_studio_url = args.lm_studio_url or os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1")
    text_model = args.text_model or profile_settings.get("text_model") or os.getenv("LM_STUDIO_MODEL", "phi-3-mini")
    vision_model = args.vision_model or profile_settings.get("vision_model") or os.getenv("LM_STUDIO_VISION_MODEL", "llava-7b-q4")
    whisper_model = args.whisper_model or profile_settings.get("whisper_model") or os.getenv("WHISPER_MODEL", "small")
    vision_on_cpu = profile_settings.get("vision_on_cpu", False)
    
    # OpenAI backward compatibility
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    openai_model = args.model or os.getenv("OPENAI_MODEL")
    openai_whisper = args.openai_whisper_model
    
    # Check if video file exists
    if not os.path.exists(args.video):
        print(f"Error: Video file not found: {args.video}")
        sys.exit(1)
    
    # Create analyzer and run
    try:
        print("=" * 60)
        print("Meeting Analyzer - Local AI Analysis")
        print("=" * 60)
        if profile_name and profile_name != "custom":
            print(f"Hardware Profile: {profile_name}")
            print(f"  {get_profile_description(profile_name)}")
        print(f"Configuration:")
        print(f"  LM Studio URL: {lm_studio_url}")
        print(f"  Text Model: {text_model}")
        print(f"  Vision Model: {vision_model} {'(CPU mode)' if vision_on_cpu else '(GPU mode)'}")
        print(f"  Whisper Model: {whisper_model}")
        if api_key and openai_model:
            print(f"  OpenAI Fallback: Enabled (using {openai_model})")
        print()
        
        analyzer = MeetingAnalyzer(
            video_path=args.video,
            lm_studio_url=lm_studio_url,
            text_model=text_model,
            vision_model=vision_model,
            whisper_model=whisper_model,
            vision_on_cpu=vision_on_cpu,
            output_dir=args.output,
            openai_api_key=api_key,
            openai_model=openai_model,
            openai_whisper_model=openai_whisper
        )
        
        results = analyzer.analyze(
            extract_frames_interval=args.interval,
            extract_key_frames=not args.no_key_frames,
            max_key_frames=args.max_frames,
            max_frames_to_analyze=args.max_analyze,
            project_name=args.project
        )
        
        print("\n✓ Analysis complete!")
        print(f"\nGenerated files:")
        if 'srs_markdown' in results:
            print(f"  - SRS (Markdown): {results['srs_markdown']}")
        if 'srs_docx' in results:
            print(f"  - SRS (DOCX): {results['srs_docx']}")
        if 'requirements_json' in results:
            print(f"  - Requirements (JSON): {results['requirements_json']}")
        
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
