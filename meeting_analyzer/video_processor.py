"""
Video processor module for extracting frames and screenshots from video files
"""

import cv2
import os
from typing import List, Tuple
from pathlib import Path
import numpy as np
from PIL import Image


class VideoProcessor:
    """Processes video files to extract key frames and screenshots"""
    
    def __init__(self, video_path: str, output_dir: str = "output/frames"):
        """
        Initialize the video processor
        
        Args:
            video_path: Path to the video file
            output_dir: Directory to save extracted frames
        """
        self.video_path = video_path
        self.output_dir = output_dir
        self.frames = []
        
        os.makedirs(output_dir, exist_ok=True)
    
    def extract_frames(self, interval_seconds: int = 5) -> List[str]:
        """
        Extract frames from video at specified intervals
        
        Args:
            interval_seconds: Time interval between frame extractions
            
        Returns:
            List of paths to extracted frame images
        """
        cap = cv2.VideoCapture(self.video_path)
        
        if not cap.isOpened():
            raise ValueError(f"Unable to open video file: {self.video_path}")
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps * interval_seconds)
        frame_count = 0
        saved_frames = []
        
        print(f"Extracting frames from video (FPS: {fps}, Interval: {interval_seconds}s)...")
        
        while True:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            if frame_count % frame_interval == 0:
                frame_path = os.path.join(
                    self.output_dir, 
                    f"frame_{frame_count:06d}.jpg"
                )
                cv2.imwrite(frame_path, frame)
                saved_frames.append(frame_path)
                self.frames.append(frame)
                print(f"  Extracted frame at {frame_count/fps:.2f}s")
            
            frame_count += 1
        
        cap.release()
        print(f"Total frames extracted: {len(saved_frames)}")
        return saved_frames
    
    def extract_key_frames(self, threshold: float = 30.0, max_frames: int = 20) -> List[str]:
        """
        Extract key frames based on scene changes
        
        Args:
            threshold: Threshold for detecting scene changes
            max_frames: Maximum number of frames to extract
            
        Returns:
            List of paths to key frame images
        """
        cap = cv2.VideoCapture(self.video_path)
        
        if not cap.isOpened():
            raise ValueError(f"Unable to open video file: {self.video_path}")
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        prev_frame = None
        frame_count = 0
        saved_frames = []
        
        print(f"Extracting key frames based on scene changes...")
        
        while len(saved_frames) < max_frames:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            if prev_frame is not None:
                # Calculate frame difference
                diff = cv2.absdiff(
                    cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
                    cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
                )
                diff_score = np.mean(diff)
                
                if diff_score > threshold:
                    frame_path = os.path.join(
                        self.output_dir,
                        f"keyframe_{len(saved_frames):04d}.jpg"
                    )
                    cv2.imwrite(frame_path, frame)
                    saved_frames.append(frame_path)
                    print(f"  Key frame at {frame_count/fps:.2f}s (diff: {diff_score:.2f})")
            
            prev_frame = frame
            frame_count += 1
        
        cap.release()
        print(f"Total key frames extracted: {len(saved_frames)}")
        return saved_frames
    
    def get_video_metadata(self) -> dict:
        """
        Get video metadata
        
        Returns:
            Dictionary with video metadata
        """
        cap = cv2.VideoCapture(self.video_path)
        
        if not cap.isOpened():
            raise ValueError(f"Unable to open video file: {self.video_path}")
        
        metadata = {
            "fps": cap.get(cv2.CAP_PROP_FPS),
            "frame_count": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "duration_seconds": cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
        }
        
        cap.release()
        return metadata
