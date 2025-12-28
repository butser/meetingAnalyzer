"""
Example usage of Meeting Analyzer Python API
"""

import os
from meeting_analyzer import MeetingAnalyzer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Example 1: Basic usage with local models (default)
print("Example 1: Basic Analysis with Local Models")
print("-" * 60)

analyzer = MeetingAnalyzer(
    video_path="path/to/your/meeting.mp4",
    output_dir="output/example1"
    # Uses default local configuration:
    # - LM Studio at http://localhost:1234/v1
    # - Text model: phi-3-mini
    # - Vision model: llava-7b-q4
    # - Whisper model: small
)

results = analyzer.analyze(project_name="Example Project")

print(f"\nGenerated SRS: {results.get('srs_markdown')}")
print(f"Requirements JSON: {results.get('requirements_json')}")


# Example 2: Custom local model configuration
print("\n\nExample 2: Custom Local Model Configuration")
print("-" * 60)

analyzer = MeetingAnalyzer(
    video_path="path/to/your/meeting.mp4",
    lm_studio_url="http://localhost:1234/v1",
    text_model="llama-3.2-3b",  # Custom text model
    vision_model="llava-7b-q4",  # Custom vision model
    whisper_model="medium",      # Use medium Whisper model
    output_dir="output/example2"
)

results = analyzer.analyze(
    extract_frames_interval=5,  # Extract frame every 5 seconds
    extract_key_frames=False,   # Disable key frame detection
    project_name="Custom Config Project"
)


# Example 3: Key frame extraction
print("\n\nExample 3: Key Frame Extraction")
print("-" * 60)

analyzer = MeetingAnalyzer(
    video_path="path/to/your/meeting.mp4",
    output_dir="output/example3"
)

results = analyzer.analyze(
    extract_key_frames=True,  # Enable key frame detection
    max_key_frames=20,        # Extract up to 20 key frames
    project_name="Key Frames Project"
)


# Example 4: Accessing detailed results
print("\n\nExample 4: Accessing Detailed Results")
print("-" * 60)

analyzer = MeetingAnalyzer(
    video_path="path/to/your/meeting.mp4",
    output_dir="output/example4"
)

results = analyzer.analyze(project_name="Detailed Analysis")

# Access transcription
if 'transcription' in results:
    print(f"\nTranscription: {results['transcription']['text'][:200]}...")

# Access video metadata
if 'video_metadata' in results:
    metadata = results['video_metadata']
    print(f"\nVideo Duration: {metadata['duration_seconds']:.2f} seconds")
    print(f"Resolution: {metadata['width']}x{metadata['height']}")
    print(f"FPS: {metadata['fps']}")

# Access requirements
if 'requirements' in results:
    print(f"\nRequirements extracted: {len(results['requirements'])} sections")


# Example 5: Backward compatibility with OpenAI (optional)
print("\n\nExample 5: Backward Compatibility with OpenAI")
print("-" * 60)

# Get API key from environment (optional)
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    analyzer = MeetingAnalyzer(
        video_path="path/to/your/meeting.mp4",
        openai_api_key=api_key,
        openai_model="gpt-4o",  # Use GPT-4o for vision/text
        openai_whisper_model="whisper-1",  # Use OpenAI Whisper
        output_dir="output/example5"
    )
    
    results = analyzer.analyze(project_name="OpenAI Project")
    print(f"Generated SRS: {results.get('srs_markdown')}")
else:
    print("Skipped: OPENAI_API_KEY not set (this is optional)")

print("\n✓ All examples complete!")
