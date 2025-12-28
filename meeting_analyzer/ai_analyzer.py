"""
AI analyzer module for combining visual and audio analysis
"""

import os
import json
from typing import List, Dict, Optional
import base64
from pathlib import Path


class AIAnalyzer:
    """Uses AI to analyze meeting content and extract requirements"""
    
    def __init__(self, 
                 lm_studio_url: str = "http://localhost:1234/v1",
                 text_model: str = "phi-3-mini",
                 vision_model: str = "llava-7b-q4",
                 vision_on_cpu: bool = False):
        """
        Initialize the AI analyzer with LM Studio
        
        Args:
            lm_studio_url: LM Studio base URL (default: http://localhost:1234/v1)
            text_model: Text model name (default: phi-3-mini)
            vision_model: Vision model name (default: llava-7b-q4)
            vision_on_cpu: Whether to run vision model on CPU (default: False)
        """
        self.lm_studio_url = lm_studio_url
        self.text_model = text_model
        self.vision_model = vision_model
        self.vision_on_cpu = vision_on_cpu
        self._cpu_mode_warned = False  # Track if we've shown the CPU mode message
        
        try:
            # Use OpenAI client library with LM Studio endpoint
            from openai import OpenAI
            self.client = OpenAI(
                base_url=lm_studio_url,
                api_key="lm-studio"  # Placeholder, not validated by LM Studio
            )
        except ImportError:
            raise ImportError(
                "OpenAI client library required for LM Studio compatibility. "
                "Install with: pip install openai"
            )
    
    def encode_image(self, image_path: str) -> str:
        """
        Encode image to base64
        
        Args:
            image_path: Path to image file
            
        Returns:
            Base64 encoded image string
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def analyze_frames(self, frame_paths: List[str]) -> List[Dict]:
        """
        Analyze video frames to extract visual information
        
        Args:
            frame_paths: List of paths to frame images
            
        Returns:
            List of analysis results for each frame
        """
        results = []
        
        print(f"Analyzing {len(frame_paths)} frames...")
        if self.vision_on_cpu and not self._cpu_mode_warned:
            print("  Note: Using CPU mode for vision analysis (may be slower)")
            self._cpu_mode_warned = True
        
        for i, frame_path in enumerate(frame_paths):
            print(f"  Analyzing frame {i+1}/{len(frame_paths)}: {frame_path}")
            
            try:
                base64_image = self.encode_image(frame_path)
                
                # Use the configured vision model (LLaVA, etc.)
                response = self.client.chat.completions.create(
                    model=self.vision_model,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": """Analyze this screenshot from a meeting recording. 
                                    Describe what you see including:
                                    - UI elements, screens, or app interfaces
                                    - Diagrams, charts, or visual aids
                                    - Text content visible
                                    - Any features or functionality being shown
                                    Be detailed and technical."""
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=500
                )
                
                analysis = response.choices[0].message.content
                results.append({
                    "frame": frame_path,
                    "analysis": analysis
                })
                
            except Exception as e:
                print(f"    Error analyzing frame: {str(e)}")
                results.append({
                    "frame": frame_path,
                    "analysis": f"Error: {str(e)}"
                })
        
        return results
    
    def generate_requirements(self, 
                            transcription: Dict,
                            frame_analyses: List[Dict]) -> Dict:
        """
        Generate SRS requirements from transcription and visual analysis
        
        Args:
            transcription: Audio transcription data
            frame_analyses: Visual frame analysis data
            
        Returns:
            Dictionary containing extracted requirements
        """
        print("Generating requirements from meeting data...")
        
        # Prepare context for AI
        visual_context = "\n\n".join([
            f"Frame {i+1}: {analysis['analysis']}"
            for i, analysis in enumerate(frame_analyses)
        ])
        
        audio_context = transcription.get('text', '')
        
        prompt = f"""You are analyzing a meeting recording to create a Software Requirements Specification (SRS).

AUDIO TRANSCRIPT:
{audio_context}

VISUAL CONTENT ANALYSIS:
{visual_context}

Based on the above meeting content, extract and organize the following:

1. PROJECT OVERVIEW
   - Project name/title
   - Purpose and objectives
   - Scope

2. FUNCTIONAL REQUIREMENTS
   - List all features and functionality mentioned
   - User stories or use cases
   - Specific capabilities required

3. NON-FUNCTIONAL REQUIREMENTS
   - Performance requirements
   - Security requirements
   - Usability requirements
   - Any other quality attributes

4. TECHNICAL REQUIREMENTS
   - Technologies mentioned
   - Platforms or frameworks
   - Integration requirements

5. ISSUES AND CONCERNS
   - Problems identified
   - Risks mentioned
   - Constraints

6. UI/UX REQUIREMENTS
   - Interface designs or mockups shown
   - User flow descriptions
   - Visual design requirements

Provide a comprehensive but concise analysis in JSON format."""

        try:
            response = self.client.chat.completions.create(
                model=self.text_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert business analyst creating Software Requirements Specifications."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=3000,
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            
            # Try to parse as JSON, fallback to text if parsing fails
            try:
                requirements = json.loads(content)
            except json.JSONDecodeError as json_error:
                # JSON parsing failed - provide structured fallback
                print(f"Note: AI response was not in JSON format, using text format")
                requirements = {
                    "raw_analysis": content,
                    "note": "AI returned text format instead of JSON"
                }
            
            print("Requirements generation complete")
            return requirements
            
        except Exception as e:
            print(f"Error generating requirements: {str(e)}")
            return {
                "error": str(e),
                "status": "failed"
            }
