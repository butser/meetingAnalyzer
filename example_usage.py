"""
Example usage of Meeting Analyzer Python API
"""

import os
from meeting_analyzer import MeetingAnalyzer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("Error: OPENAI_API_KEY not found in environment")
    print("Please set it in .env file or as environment variable")
    exit(1)

# Example 1: Basic usage
print("Example 1: Basic Analysis")
print("-" * 60)

analyzer = MeetingAnalyzer(
    video_path="path/to/your/meeting.mp4",
    openai_api_key=api_key,
    output_dir="output/example1"
)

results = analyzer.analyze(project_name="Example Project")

print(f"\nGenerated SRS: {results.get('srs_markdown')}")
print(f"Requirements JSON: {results.get('requirements_json')}")


# Example 2: Custom configuration
print("\n\nExample 2: Custom Configuration")
print("-" * 60)

analyzer = MeetingAnalyzer(
    video_path="path/to/your/meeting.mp4",
    openai_api_key=api_key,
    output_dir="output/example2",
    openai_model="gpt-4o",  # Use GPT-4o for better vision analysis
    whisper_model="whisper-1"
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
    openai_api_key=api_key,
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
    openai_api_key=api_key,
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

print("\n✓ All examples complete!")
