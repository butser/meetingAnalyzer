# Meeting Analyzer GUI Documentation

## Overview

The Meeting Analyzer GUI provides a comprehensive graphical user interface for the Meeting Analyzer application. It exposes all CLI parameters in an easy-to-use interface with real-time progress updates and error handling.

## Features

### Input Parameters
- **Video File Selection**: Browse button for easy file selection
- **Hardware Profile Selector**: Choose between laptop, pc, or custom profiles
- **LM Studio Configuration**: Configure LM Studio URL and model names
  - Text Model (default: phi-3-mini)
  - Vision Model (default: llava-7b-q4)
  - Whisper Model (dropdown: tiny/base/small/medium/large)

### Project Settings
- **Project Name**: Set the name for your SRS document
- **Output Directory**: Choose where to save generated files

### Frame Extraction Options
- **Use Key Frames**: Toggle scene change detection
- **Extraction Interval**: Set interval for frame extraction (1-60 seconds)
- **Max Key Frames**: Limit the number of key frames (1-100)
- **Max Frames to Analyze**: Limit frames sent to AI (1-50)

### Progress and Status
- **Progress Bar**: Visual indicator showing analysis progress (0-100%)
- **Status Label**: Real-time text showing current step
- **Detailed Log**: Scrollable text area with color-coded messages
  - Blue: Informational messages
  - Green: Success messages
  - Red: Error messages

### Control Buttons
- **Start Analysis**: Begin the analysis process
- **Stop Analysis**: Cancel ongoing analysis
- **Clear Log**: Clear the log output
- **Open Output Folder**: Open output directory in file explorer

### Results Section
- **Generated Files**: Shows paths to generated files after completion
  - SRS Markdown file
  - SRS DOCX file
  - Requirements JSON file
- **Open Buttons**: Click to open files in default applications

## Installation

The GUI is automatically installed with the Meeting Analyzer package:

```bash
pip install -e .
```

## Usage

Launch the GUI from the command line:

```bash
meeting-analyzer-gui
```

### Step-by-Step Guide

1. **Select Video File**
   - Click "Browse..." next to Video File
   - Select your meeting video file (.mp4, .avi, .mov, .mkv, .webm)

2. **Choose Hardware Profile**
   - Select "Laptop" for limited VRAM (4GB)
   - Select "PC" for high-end hardware (24GB VRAM)
   - Select "Custom" to manually configure all settings

3. **Configure LM Studio**
   - Ensure LM Studio is running (default: http://localhost:1234/v1)
   - Verify model names match your loaded models
   - Adjust Whisper model size based on your needs

4. **Set Project Settings**
   - Enter a descriptive project name
   - Choose output directory (default: ./output)

5. **Adjust Frame Extraction**
   - Keep "Use Key Frames" checked for intelligent scene detection
   - Or uncheck and set interval for regular frame extraction
   - Adjust max frames based on video length and detail needed

6. **Start Analysis**
   - Click "Start Analysis"
   - Monitor progress in the progress bar and log
   - Wait for completion (can take several minutes)

7. **Access Results**
   - Click "Open" buttons to view generated files
   - Or click "Open Output Folder" to browse all files

## Error Handling

The GUI displays clear error messages for common issues:

- **Missing Video File**: Prompts to select a valid file
- **FFmpeg Not Installed**: Shows error with installation instructions
- **LM Studio Connection Error**: Displays connection failure details
- **Model Not Found**: Shows which model is missing
- **CUDA/GPU Errors**: Indicates GPU-related problems

All errors are displayed in:
- Status label (top of error message)
- Detailed log (with red highlighting)
- Popup dialog (for critical errors)

## Background Processing

The GUI runs analysis in a separate thread to keep the interface responsive:

- You can scroll the log while analysis is running
- The progress bar updates in real-time
- The "Stop Analysis" button allows cancellation at any time

## Advanced Features

### Configuration Persistence

Settings from environment variables (.env file) are automatically loaded:
- LM_STUDIO_URL
- LM_STUDIO_MODEL
- LM_STUDIO_VISION_MODEL
- WHISPER_MODEL

### Platform Support

The GUI works on all platforms:
- **Windows**: Opens files with default applications
- **macOS**: Uses 'open' command
- **Linux**: Uses 'xdg-open' command

## Technical Details

### Architecture
- **GUI Framework**: Tkinter (Python standard library)
- **Threading**: Background thread for analysis
- **Message Queue**: Thread-safe communication between GUI and analyzer
- **Progress Callbacks**: Real-time updates from analyzer to GUI

### Code Structure
```python
MeetingAnalyzerGUI
├── setup_ui()              # Create all GUI elements
├── start_analysis()        # Start background analysis thread
├── stop_analysis()         # Request cancellation
├── update_progress()       # Update progress bar and status
├── analysis_complete()     # Handle completion
└── process_queue()         # Process messages from background thread
```

## Troubleshooting

### GUI Won't Launch
- **Issue**: "no display name and no $DISPLAY environment variable"
- **Solution**: You're in a headless environment. Use the CLI instead:
  ```bash
  meeting-analyzer --video video.mp4
  ```

### Analysis Stops Unexpectedly
- Check the detailed log for error messages
- Verify LM Studio is running and accessible
- Ensure FFmpeg is installed for audio processing
- Check that you have sufficient disk space

### Results Not Generated
- Verify all steps completed successfully in the log
- Check output directory permissions
- Look for error messages in red

## Examples

### Basic Analysis with GUI
1. Launch: `meeting-analyzer-gui`
2. Select video file
3. Choose "Laptop" profile
4. Click "Start Analysis"
5. Wait for completion
6. Click "Open" on SRS Markdown to view results

### Custom Configuration
1. Launch GUI
2. Select "Custom" profile
3. Set LM Studio URL to custom endpoint
4. Configure specific models
5. Adjust frame extraction to extract every 5 seconds
6. Start analysis

## Comparison: GUI vs CLI

| Feature | GUI | CLI |
|---------|-----|-----|
| Ease of Use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Progress Visibility | Real-time progress bar | Text output |
| Error Handling | Popup dialogs + log | Text output |
| File Access | One-click open buttons | Manual navigation |
| Automation | Manual operation | Scriptable |
| Remote Access | Requires X11 forwarding | SSH-friendly |

Use the **GUI** for:
- Interactive analysis
- Learning the tool
- One-off analyses
- Visual progress monitoring

Use the **CLI** for:
- Automated workflows
- Remote/headless servers
- Batch processing
- CI/CD integration
