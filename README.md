# Meeting Analyzer

AI-powered tool that analyzes meeting recordings to automatically generate Software Requirements Specification (SRS) documentation using **local AI models** - no internet or API costs required!

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
- 🎤 **Local Audio Transcription**: GPU-accelerated Whisper model (faster-whisper)
- 🤖 **Local AI Analysis**: LM Studio with vision and text models
- 📄 **Multiple Output Formats**: Markdown, DOCX, and JSON
- 🔧 **Configurable**: Flexible options for customization
- 💰 **Free**: No API costs, works completely offline
- 🚀 **Privacy-First**: All processing happens locally on your machine

## Installation

### Prerequisites

- Python 3.8 or higher
- FFmpeg (for audio extraction)
- LM Studio (for local AI analysis)
- GPU recommended (GTX 1050 Ti or better) but not required

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

## Setup LM Studio

1. **Download LM Studio**: Visit [lmstudio.ai](https://lmstudio.ai/) and download for your platform
2. **Install LM Studio**: Follow the installation instructions
3. **Download Models**: 
   - For **Text Analysis**: Download Phi-3 Mini or Llama 3.2 3B (fits in 4GB VRAM)
   - For **Vision Analysis**: Download LLaVA 7B Q4 (can run on CPU with 48GB RAM)
4. **Start Server**: 
   - Open LM Studio
   - Go to "Local Server" tab
   - Load your chosen model
   - Click "Start Server" (default: http://localhost:1234)

### Recommended Models for Limited Hardware (4GB VRAM)

**Hardware Profile: GTX 1050 Ti (4GB), 48GB RAM, i5-8300H**

| Model Type | Recommended | Size | Where it Runs | Notes |
|------------|-------------|------|---------------|-------|
| Text | Phi-3 Mini | ~2GB | GPU | Fast, good for analysis |
| Text | Llama 3.2 3B | ~2GB | GPU | Alternative to Phi-3 |
| Vision | LLaVA 7B Q4 | ~4GB | CPU | Use with 48GB RAM |
| Whisper | small | ~500MB | GPU | Good accuracy, fits VRAM |

**Setup Tips:**
- Load **text model** in LM Studio for requirements generation (runs on GPU)
- Load **vision model** when analyzing frames (will use CPU with your RAM)
- **Whisper small** model runs automatically on GPU during transcription
- You may need to restart LM Studio to switch between models

## Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` if you want to customize (optional):
```env
# Hardware Profile: laptop or pc
HARDWARE_PROFILE=laptop

# LM Studio Configuration
LM_STUDIO_URL=http://localhost:1234/v1

# Override specific models (optional)
# If not specified, profile settings will be used
# WHISPER_MODEL=small
# LM_STUDIO_MODEL=phi-3-mini-4k-instruct
# LM_STUDIO_VISION_MODEL=llava-v1.6-mistral-7b
```

## Usage

## Hardware Profiles

Choose a profile based on your hardware to automatically configure optimal models:

### Laptop Profile (4GB VRAM)
Optimized for GTX 1050 Ti (4GB VRAM), 48GB RAM, i5-8300H

```bash
meeting-analyzer --video meeting.mp4 --profile laptop
```

**Models used:**
- **Whisper**: small (GPU) - Fast transcription with good accuracy
- **Vision**: LLaVA 7B (CPU) - Vision analysis using system RAM
- **Text**: Phi-3 Mini (GPU) - Efficient requirements generation

### PC Profile (24GB VRAM)
Optimized for RTX 4090 (24GB VRAM), 96GB RAM, i7-12xxx

```bash
meeting-analyzer --video meeting.mp4 --profile pc
```

**Models used:**
- **Whisper**: large-v3 (GPU) - Highest accuracy transcription
- **Vision**: LLaVA 34B (GPU) - Advanced vision analysis
- **Text**: Llama 3.1 70B (GPU) - Professional-grade requirements

### Custom Settings
Override individual settings while using a profile:

```bash
# Use laptop profile but upgrade Whisper model
meeting-analyzer --video meeting.mp4 --profile laptop --whisper-model medium

# Use PC profile with custom vision model
meeting-analyzer --video meeting.mp4 --profile pc --vision-model llava-v1.6-mistral-7b
```

Or use custom profile for complete manual control:

```bash
meeting-analyzer --video meeting.mp4 --profile custom --whisper-model small --text-model phi-3-mini
```

### Basic Usage

```bash
# Analyze a meeting video (uses default local models)
meeting-analyzer --video path/to/meeting.mp4
```

### Advanced Options

```bash
# Specify project name and output directory
meeting-analyzer --video meeting.mp4 --project "Mobile App Project" --output ./results

# Use different local Whisper model
meeting-analyzer --video meeting.mp4 --whisper-model medium

# Use custom LM Studio URL
meeting-analyzer --video meeting.mp4 --lm-studio-url http://localhost:1234/v1

# Specify custom models
meeting-analyzer --video meeting.mp4 --text-model llama-3.2-3b --vision-model llava-7b

# Extract frames at specific intervals
meeting-analyzer --video meeting.mp4 --interval 5 --no-key-frames

# Set maximum number of key frames
meeting-analyzer --video meeting.mp4 --max-frames 20
```

### Command-Line Options

```
--video VIDEO              Path to the meeting video file (required)
--profile PROFILE         Hardware profile: laptop (4GB VRAM) / pc (24GB VRAM) / custom
--lm-studio-url URL       LM Studio base URL (default: http://localhost:1234/v1)
--text-model MODEL        Text model name (default: from profile or phi-3-mini)
--vision-model MODEL      Vision model name (default: from profile or llava-7b-q4)
--whisper-model SIZE      Local Whisper model: tiny/base/small/medium/large (default: from profile or small)
--project PROJECT         Project name for SRS document
--output OUTPUT           Output directory (default: ./output)
--interval SECONDS        Frame extraction interval (default: 10)
--no-key-frames          Use interval extraction instead of key frames
--max-frames N           Maximum key frames to extract (default: 15)
```

### Python API

```python
from meeting_analyzer import MeetingAnalyzer

# Initialize analyzer with local models
analyzer = MeetingAnalyzer(
    video_path="meeting.mp4",
    lm_studio_url="http://localhost:1234/v1",
    text_model="phi-3-mini",
    vision_model="llava-7b-q4",
    whisper_model="small",
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
│   ├── ai_analyzer.py       # AI-powered analysis (LM Studio)
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
   - Transcribes locally using faster-whisper (GPU accelerated)

3. **AI Analysis**
   - Analyzes visual content using LM Studio vision model (LLaVA)
   - Analyzes audio transcription using LM Studio text model (Phi-3/Llama)
   - Combines both sources to extract comprehensive requirements

4. **Document Generation**
   - Creates structured SRS document
   - Organizes requirements into categories
   - Generates multiple output formats

## Requirements

See `requirements.txt` for full dependency list:
- `openai` - OpenAI client library (required for LM Studio compatibility)
- `faster-whisper` - Local Whisper transcription
- `opencv-python` - Video processing
- `python-docx` - DOCX generation
- `Pillow` - Image processing
- `python-dotenv` - Environment variable management

**Note:** While we use the `openai` Python package, it's configured to connect to LM Studio (local), not OpenAI's cloud services. No OpenAI API key or internet connection required.

## Advantages of Local Processing

✅ **No API Costs**: Completely free after initial setup  
✅ **Privacy**: Your data never leaves your machine  
✅ **Offline**: Works without internet connection  
✅ **No Rate Limits**: Process as many meetings as you want  
✅ **Customizable**: Use any compatible local model  

## Troubleshooting

**"ffmpeg not found"**
- Install FFmpeg (see Installation section)
- Ensure FFmpeg is in your system PATH

**"Connection refused" or "LM Studio not responding"**
- Ensure LM Studio is running
- Check that the server is started in LM Studio
- Verify the URL matches (default: http://localhost:1234)
- Check firewall settings

**"Model not found" errors**
- Load the appropriate model in LM Studio before running
- Ensure model name matches exactly
- Check LM Studio's loaded models list

**"CUDA out of memory" errors**
- Use smaller models (Phi-3 Mini instead of larger models)
- For vision: Use CPU mode by setting device in LM Studio
- Reduce `--max-analyze` to analyze fewer frames
- Use `--whisper-model base` or `tiny` for smaller VRAM footprint

**Slow transcription**
- Ensure CUDA is available: `python -c "import torch; print(torch.cuda.is_available())"`
- Install CUDA toolkit if needed
- Use smaller Whisper model if necessary

**Vision model too slow**
- LLaVA on CPU is slower but works with 48GB RAM
- Reduce number of frames with `--max-analyze 5`
- Consider using interval-based extraction for fewer frames

## Performance Tips

**For 4GB VRAM (GTX 1050 Ti):**
- Text model (Phi-3 Mini): Runs on GPU, fast
- Vision model (LLaVA 7B Q4): Runs on CPU, slower but works
- Whisper (small): Runs on GPU, fast
- Transcription: ~1-2x realtime (10 min audio = 5-10 min processing)
- Vision analysis: ~30-60 seconds per frame on CPU
- Text analysis: ~10-30 seconds on GPU

**Optimization:**
- Use `--max-analyze 5` to reduce frame analysis time
- Use `--whisper-model small` for best speed/quality balance
- Extract fewer key frames with `--max-frames 10`

## Backward Compatibility

The tool still supports OpenAI APIs for backward compatibility:

```bash
# Use OpenAI (optional)
meeting-analyzer --video meeting.mp4 --api-key YOUR_KEY --model gpt-4o --openai-whisper whisper-1
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is available for use under standard open source practices.

## Support

For issues and questions, please open an issue on GitHub.