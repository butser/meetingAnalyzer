# Meeting Analyzer

AI-powered tool that analyzes meeting recordings to automatically generate Software Requirements Specification (SRS) documentation.

## Overview

Meeting Analyzer processes video files containing:
- **Visual Content**: App screens, screenshots, diagrams, and UI mockups
- **Audio Content**: Discussion of requirements, features, and issues

It produces comprehensive SRS documentation including:
- Functional requirements
- Non-functional requirements
- Technical specifications
- UI/UX requirements
- Issues and concerns

## Features

- 🎥 **Video Frame Extraction**: Intelligent key frame detection or interval-based extraction
- 🎤 **Audio Transcription**: OpenAI Whisper-powered speech-to-text
- 🤖 **AI-Powered Analysis**: GPT-4 vision and text analysis
- 📄 **Multiple Output Formats**: Markdown, DOCX, and JSON
- 🔧 **Configurable**: Flexible options for customization

## Installation

### Prerequisites

- Python 3.8 or higher
- FFmpeg (for audio extraction)
- OpenAI API key

### Install FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html)

### Install Meeting Analyzer

```bash
# Clone the repository
git clone https://github.com/butser/meetingAnalyzer.git
cd meetingAnalyzer

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

## Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

### Basic Usage

```bash
meeting-analyzer --video path/to/meeting.mp4
```

### Advanced Options

```bash
# Specify project name and output directory
meeting-analyzer --video meeting.mp4 --project "Mobile App Project" --output ./results

# Use custom OpenAI model
meeting-analyzer --video meeting.mp4 --model gpt-4o

# Extract frames at specific intervals
meeting-analyzer --video meeting.mp4 --interval 5 --no-key-frames

# Set maximum number of key frames
meeting-analyzer --video meeting.mp4 --max-frames 20
```

### Command-Line Options

```
--video VIDEO          Path to the meeting video file (required)
--api-key API_KEY      OpenAI API key (or set OPENAI_API_KEY env var)
--project PROJECT      Project name for SRS document
--output OUTPUT        Output directory (default: ./output)
--model MODEL          OpenAI model (default: gpt-4-turbo-preview)
--whisper-model MODEL  Whisper model (default: whisper-1)
--interval SECONDS     Frame extraction interval (default: 10)
--no-key-frames        Use interval extraction instead of key frames
--max-frames N         Maximum key frames to extract (default: 15)
```

### Python API

```python
from meeting_analyzer import MeetingAnalyzer

# Initialize analyzer
analyzer = MeetingAnalyzer(
    video_path="meeting.mp4",
    openai_api_key="your_api_key",
    output_dir="output"
)

# Run analysis
results = analyzer.analyze(
    project_name="My Project",
    extract_key_frames=True,
    max_key_frames=15
)

# Access results
print(f"SRS Document: {results['srs_markdown']}")
print(f"Requirements: {results['requirements']}")
```

## Output

The tool generates several output files:

1. **SRS Document (Markdown)**: `SRS_Project_Name.md`
   - Comprehensive requirements specification
   - Organized into standard SRS sections

2. **SRS Document (DOCX)**: `SRS_Project_Name.docx`
   - Microsoft Word format for editing
   - Professional formatting

3. **Requirements JSON**: `requirements_Project_Name.json`
   - Structured data for further processing
   - Machine-readable format

4. **Analysis Results**: `analysis_results.json`
   - Complete analysis metadata
   - Transcription and frame analysis data

5. **Extracted Frames**: `frames/` directory
   - Key frames or interval frames from video

6. **Audio Files**: `audio/` directory
   - Extracted audio and transcription

## Project Structure

```
meetingAnalyzer/
├── meeting_analyzer/
│   ├── __init__.py
│   ├── analyzer.py          # Main orchestrator
│   ├── video_processor.py   # Video frame extraction
│   ├── audio_processor.py   # Audio extraction & transcription
│   ├── ai_analyzer.py       # AI-powered analysis
│   ├── srs_generator.py     # SRS document generation
│   └── cli.py               # Command-line interface
├── requirements.txt
├── setup.py
├── .env.example
├── .gitignore
└── README.md
```

## How It Works

1. **Video Processing**
   - Extracts key frames using scene change detection
   - Or extracts frames at regular intervals

2. **Audio Processing**
   - Extracts audio track from video using FFmpeg
   - Transcribes audio using OpenAI Whisper API

3. **AI Analysis**
   - Analyzes visual content (screenshots, diagrams, UI)
   - Analyzes audio transcription (requirements, discussions)
   - Combines both sources to extract comprehensive requirements

4. **Document Generation**
   - Creates structured SRS document
   - Organizes requirements into categories
   - Generates multiple output formats

## Requirements

See `requirements.txt` for full dependency list:
- `openai` - OpenAI API integration
- `opencv-python` - Video processing
- `python-docx` - DOCX generation
- `Pillow` - Image processing
- `python-dotenv` - Environment variable management

## Cost Considerations

This tool uses OpenAI's APIs which have associated costs:
- **Whisper API**: ~$0.006 per minute of audio
- **GPT-4 Vision**: ~$0.01-0.03 per image
- **GPT-4 Text**: ~$0.01-0.03 per 1K tokens

A typical 30-minute meeting might cost $1-3 to analyze.

## Limitations

- Requires clear audio for accurate transcription
- Visual analysis quality depends on image clarity
- API costs scale with meeting length
- Requires internet connection for OpenAI APIs

## Troubleshooting

**"ffmpeg not found"**
- Install FFmpeg (see Installation section)
- Ensure FFmpeg is in your system PATH

**"OpenAI API key required"**
- Set `OPENAI_API_KEY` in `.env` file
- Or pass `--api-key` argument

**"Unable to open video file"**
- Check video file path is correct
- Ensure video format is supported (MP4, AVI, MOV, etc.)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is available for use under standard open source practices.

## Support

For issues and questions, please open an issue on GitHub.