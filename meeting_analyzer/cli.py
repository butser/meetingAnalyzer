"""
Command-line interface for Meeting Analyzer
"""

import argparse
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from .analyzer import MeetingAnalyzer


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Meeting Analyzer - AI-powered tool to analyze meeting videos and generate SRS documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with video file
  meeting-analyzer --video meeting.mp4 --api-key YOUR_API_KEY
  
  # Use environment variable for API key
  export OPENAI_API_KEY=your_key
  meeting-analyzer --video meeting.mp4
  
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
    
    # Optional arguments
    parser.add_argument(
        "--api-key",
        help="OpenAI API key (or set OPENAI_API_KEY environment variable)"
    )
    
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
    
    parser.add_argument(
        "--model",
        default="gpt-4-turbo-preview",
        help="OpenAI model to use (default: gpt-4-turbo-preview)"
    )
    
    parser.add_argument(
        "--whisper-model",
        default="whisper-1",
        help="Whisper model for transcription (default: whisper-1)"
    )
    
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
        help="Maximum number of frames to analyze with AI for cost control (default: 10)"
    )
    
    args = parser.parse_args()
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key from args or environment
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: OpenAI API key required!")
        print("Provide it via --api-key argument or OPENAI_API_KEY environment variable")
        print("\nSet up:")
        print("  1. Copy .env.example to .env")
        print("  2. Add your OpenAI API key to .env")
        print("  3. Run the command again")
        sys.exit(1)
    
    # Check if video file exists
    if not os.path.exists(args.video):
        print(f"Error: Video file not found: {args.video}")
        sys.exit(1)
    
    # Create analyzer and run
    try:
        analyzer = MeetingAnalyzer(
            video_path=args.video,
            openai_api_key=api_key,
            output_dir=args.output,
            openai_model=args.model,
            whisper_model=args.whisper_model
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
