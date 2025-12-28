"""
Meeting Analyzer - AI-powered meeting analysis tool
Processes video and audio to generate Software Requirements Specification (SRS) documents
"""

__version__ = "1.0.0"
__author__ = "Meeting Analyzer Team"

from .analyzer import MeetingAnalyzer
from .video_processor import VideoProcessor
from .audio_processor import AudioProcessor
from .ai_analyzer import AIAnalyzer
from .srs_generator import SRSGenerator

__all__ = [
    'MeetingAnalyzer',
    'VideoProcessor',
    'AudioProcessor',
    'AIAnalyzer',
    'SRSGenerator',
]
