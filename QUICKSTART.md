# Quick Start Guide

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/butser/meetingAnalyzer.git
cd meetingAnalyzer
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install FFmpeg** (required for audio extraction):

   - **macOS:** `brew install ffmpeg`
   - **Ubuntu/Debian:** `sudo apt-get install ffmpeg`
   - **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html)

4. **Set up API key:**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Basic Usage

```bash
# Run analysis on a meeting video
meeting-analyzer --video path/to/meeting.mp4

# Specify a project name
meeting-analyzer --video meeting.mp4 --project "My Mobile App"

# Use custom output directory
meeting-analyzer --video meeting.mp4 --output ./my-results
```

## What You'll Get

After running the analyzer, you'll find these files in the output directory:

1. **SRS_Project_Name.md** - Comprehensive requirements document in Markdown
2. **SRS_Project_Name.docx** - Same document in Microsoft Word format
3. **requirements_Project_Name.json** - Structured data in JSON format
4. **analysis_results.json** - Complete analysis metadata
5. **frames/** - Extracted video frames
6. **audio/** - Extracted audio and transcription

## Example Output Structure

```
output/
├── SRS_My_Project.md
├── SRS_My_Project.docx
├── requirements_My_Project.json
├── analysis_results.json
├── frames/
│   ├── keyframe_0001.jpg
│   ├── keyframe_0002.jpg
│   └── ...
└── audio/
    ├── meeting.wav
    └── meeting_transcript.json
```

## Using the Python API

```python
from meeting_analyzer import MeetingAnalyzer

# Create analyzer
analyzer = MeetingAnalyzer(
    video_path="meeting.mp4",
    openai_api_key="your-api-key",
    output_dir="output"
)

# Run analysis
results = analyzer.analyze(project_name="My Project")

# Get the generated SRS document path
print(results['srs_markdown'])
```

## Common Issues

### FFmpeg Not Found
If you see "ffmpeg not found", install FFmpeg:
- macOS: `brew install ffmpeg`
- Ubuntu: `sudo apt-get install ffmpeg`
- Windows: Download and add to PATH

### API Key Error
Make sure your OpenAI API key is set:
1. Copy `.env.example` to `.env`
2. Add your API key to `.env`
3. Or pass it via `--api-key` argument

### Video Format Not Supported
Supported formats: MP4, AVI, MOV, MKV, FLV, WMV

If your video doesn't work, try converting to MP4:
```bash
ffmpeg -i input.avi output.mp4
```

## Cost Estimate

OpenAI API costs for a typical 30-minute meeting:
- Audio transcription (Whisper): ~$0.18
- Frame analysis (GPT-4 Vision): ~$0.30 (for 10 frames)
- Requirements generation (GPT-4): ~$0.10

**Total: ~$0.60 - $3.00** depending on video length and settings

## Next Steps

1. Try the analyzer on a sample meeting video
2. Review the generated SRS document
3. Customize settings for your needs
4. Integrate into your documentation workflow

For more details, see the main [README.md](README.md).
