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

4. **Set up LM Studio** (for local AI analysis):

   a. Download and install [LM Studio](https://lmstudio.ai/)
   
   b. Download recommended models:
      - **Text**: Phi-3 Mini or Llama 3.2 3B
      - **Vision**: LLaVA 7B Q4
   
   c. Start the LM Studio server:
      - Open LM Studio
      - Go to "Local Server" tab
      - Load your text model
      - Click "Start Server" (http://localhost:1234)

5. **Configure (optional):**
```bash
cp .env.example .env
# Edit .env to customize model settings if needed
```

## Basic Usage

```bash
# Run analysis on a meeting video (uses local AI models)
meeting-analyzer --video path/to/meeting.mp4

# Specify a project name
meeting-analyzer --video meeting.mp4 --project "My Mobile App"

# Use custom output directory
meeting-analyzer --video meeting.mp4 --output ./my-results

# Use different Whisper model
meeting-analyzer --video meeting.mp4 --whisper-model medium
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

# Create analyzer with local models (default)
analyzer = MeetingAnalyzer(
    video_path="meeting.mp4",
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

### LM Studio Connection Error
Make sure LM Studio is running:
1. Open LM Studio
2. Load a model (text or vision depending on which step failed)
3. Start the local server
4. Verify it's accessible at http://localhost:1234

### CUDA Out of Memory
If you see GPU memory errors:
- Use smaller models (Phi-3 Mini instead of larger models)
- Use `--whisper-model small` or `tiny`
- Reduce `--max-analyze` to analyze fewer frames
- For vision: Let LLaVA run on CPU (it will automatically)

### Video Format Not Supported
Supported formats: MP4, AVI, MOV, MKV, FLV, WMV

If your video doesn't work, try converting to MP4:
```bash
ffmpeg -i input.avi output.mp4
```

## Hardware Requirements

**Recommended for best experience:**
- GPU: GTX 1050 Ti (4GB VRAM) or better
- RAM: 16GB+ (48GB for CPU-based vision models)
- Storage: 10GB+ for models

**What runs where with 4GB VRAM:**
- Text model (Phi-3 Mini): GPU (~2GB)
- Vision model (LLaVA 7B Q4): CPU with 48GB RAM
- Whisper small: GPU (~500MB)

## Performance

For a typical 30-minute meeting:
- Audio transcription: ~5-10 minutes (GPU) or ~30 minutes (CPU)
- Frame analysis: ~30-60 seconds per frame (LLaVA on CPU)
- Requirements generation: ~10-30 seconds (Phi-3 on GPU)

**Total time:** ~20-40 minutes depending on hardware

## Advantages

✅ **No API Costs** - Completely free after setup  
✅ **Privacy** - All processing happens locally  
✅ **Offline** - No internet required  
✅ **No Rate Limits** - Process unlimited meetings  

## Next Steps

1. Try the analyzer on a sample meeting video
2. Review the generated SRS document
3. Customize settings for your needs (model sizes, frame extraction)
4. Integrate into your documentation workflow

For more details, see the main [README.md](README.md).
