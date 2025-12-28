"""
Example usage of Meeting Analyzer Python API
"""

import os
from meeting_analyzer import MeetingAnalyzer
from meeting_analyzer.profiles import get_profile
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Example 1: Using Hardware Profile (Laptop)
print("Example 1: Using Laptop Hardware Profile")
print("-" * 60)

# Load laptop profile settings
laptop_profile = get_profile("laptop")

analyzer = MeetingAnalyzer(
    video_path="path/to/your/meeting.mp4",
    text_model=laptop_profile["text_model"],
    vision_model=laptop_profile["vision_model"],
    whisper_model=laptop_profile["whisper_model"],
    vision_on_cpu=laptop_profile["vision_on_cpu"],
    output_dir="output/example1"
)

results = analyzer.analyze(project_name="Laptop Profile Example")
print(f"\nGenerated SRS: {results.get('srs_markdown')}")
print(f"Requirements JSON: {results.get('requirements_json')}")


# Example 2: Using Hardware Profile (PC)
print("\n\nExample 2: Using PC Hardware Profile")
print("-" * 60)

# Load PC profile settings
pc_profile = get_profile("pc")

analyzer = MeetingAnalyzer(
    video_path="path/to/your/meeting.mp4",
    text_model=pc_profile["text_model"],
    vision_model=pc_profile["vision_model"],
    whisper_model=pc_profile["whisper_model"],
    vision_on_cpu=pc_profile["vision_on_cpu"],
    output_dir="output/example2"
)

results = analyzer.analyze(project_name="PC Profile Example")


# Example 3: Basic usage with local models (default)
print("\n\nExample 3: Basic Analysis with Local Models (Default)")
print("-" * 60)

analyzer = MeetingAnalyzer(
    video_path="path/to/your/meeting.mp4",
    output_dir="output/example3"
    # Uses default local configuration:
    # - LM Studio at http://localhost:1234/v1
    # - Text model: phi-3-mini
    # - Vision model: llava-7b-q4
    # - Whisper model: small
)

results = analyzer.analyze(project_name="Example Project")

print(f"\nGenerated SRS: {results.get('srs_markdown')}")
print(f"Requirements JSON: {results.get('requirements_json')}")


# Example 4: Custom local model configuration with override
print("\n\nExample 4: Profile with Override")
print("-" * 60)

# Load laptop profile but override whisper model
laptop_profile = get_profile("laptop")

analyzer = MeetingAnalyzer(
    video_path="path/to/your/meeting.mp4",
    lm_studio_url="http://localhost:1234/v1",
    text_model=laptop_profile["text_model"],
    vision_model=laptop_profile["vision_model"],
    whisper_model="medium",  # Override: use medium instead of small
    vision_on_cpu=laptop_profile["vision_on_cpu"],
    output_dir="output/example4"
)

results = analyzer.analyze(
    extract_frames_interval=5,  # Extract frame every 5 seconds
    extract_key_frames=False,   # Disable key frame detection
    project_name="Custom Config Project"
)


# Example 5: Key frame extraction
print("\n\nExample 5: Key Frame Extraction")
print("-" * 60)

analyzer = MeetingAnalyzer(
    video_path="path/to/your/meeting.mp4",
    output_dir="output/example5"
)

results = analyzer.analyze(
    extract_key_frames=True,  # Enable key frame detection
    max_key_frames=20,        # Extract up to 20 key frames
    project_name="Key Frames Project"
)


# Example 6: Accessing detailed results
print("\n\nExample 6: Accessing Detailed Results")
print("-" * 60)

analyzer = MeetingAnalyzer(
    video_path="path/to/your/meeting.mp4",
    output_dir="output/example6"
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


# Example 7: Backward compatibility with OpenAI (optional)
print("\n\nExample 7: Backward Compatibility with OpenAI")
print("-" * 60)

# Get API key from environment (optional)
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    analyzer = MeetingAnalyzer(
        video_path="path/to/your/meeting.mp4",
        openai_api_key=api_key,
        openai_model="gpt-4o",  # Use GPT-4o for vision/text
        openai_whisper_model="whisper-1",  # Use OpenAI Whisper
        output_dir="output/example7"
    )
    
    results = analyzer.analyze(project_name="OpenAI Project")
    print(f"Generated SRS: {results.get('srs_markdown')}")
else:
    print("Skipped: OPENAI_API_KEY not set (this is optional)")

print("\n✓ All examples complete!")
