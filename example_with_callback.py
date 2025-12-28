#!/usr/bin/env python3
"""
Example: Using MeetingAnalyzer with Progress Callback

This example demonstrates how to use the MeetingAnalyzer with a custom
progress callback function for programmatic integration.
"""

from meeting_analyzer.analyzer import MeetingAnalyzer


def progress_callback(step, total_steps, message, error=None):
    """
    Custom progress callback function
    
    Args:
        step: Current step number (1-based)
        total_steps: Total number of steps
        message: Status message
        error: Error message (if any)
    """
    percentage = (step / total_steps) * 100
    
    if error:
        print(f"[{percentage:.0f}%] ERROR in {message}: {error}")
    else:
        print(f"[{percentage:.0f}%] {message}")


def main():
    """Example usage with progress callback"""
    # Configuration
    video_path = "path/to/your/meeting.mp4"
    
    print("Meeting Analyzer - Progress Callback Example")
    print("=" * 60)
    print()
    
    # Create analyzer with progress callback
    analyzer = MeetingAnalyzer(
        video_path=video_path,
        lm_studio_url="http://localhost:1234/v1",
        text_model="phi-3-mini",
        vision_model="llava-7b-q4",
        whisper_model="small",
        output_dir="./output",
        progress_callback=progress_callback  # Add callback here
    )
    
    # Run analysis - progress updates will be printed via callback
    try:
        results = analyzer.analyze(
            extract_frames_interval=10,
            extract_key_frames=True,
            max_key_frames=15,
            max_frames_to_analyze=10,
            project_name="Example Project"
        )
        
        print()
        print("Analysis complete!")
        print(f"Generated files:")
        if 'srs_markdown' in results:
            print(f"  - {results['srs_markdown']}")
        if 'srs_docx' in results:
            print(f"  - {results['srs_docx']}")
        if 'requirements_json' in results:
            print(f"  - {results['requirements_json']}")
            
    except Exception as e:
        print(f"Error during analysis: {e}")


if __name__ == "__main__":
    main()
