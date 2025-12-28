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
    
    def __init__(self, api_key: str, model: str = "gpt-4-turbo-preview"):
        """
        Initialize the AI analyzer
        
        Args:
            api_key: OpenAI API key
            model: OpenAI model to use
        """
        self.api_key = api_key
        self.model = model
        
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("OpenAI library not installed. Install with: pip install openai")
    
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
        
        for i, frame_path in enumerate(frame_paths):
            print(f"  Analyzing frame {i+1}/{len(frame_paths)}: {frame_path}")
            
            try:
                base64_image = self.encode_image(frame_path)
                
                response = self.client.chat.completions.create(
                    model="gpt-4o" if "gpt-4o" in self.model else "gpt-4-turbo",
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
                model=self.model,
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
            
            # Try to parse as JSON, fallback to text
            try:
                requirements = json.loads(content)
            except json.JSONDecodeError:
                requirements = {
                    "raw_analysis": content
                }
            
            print("Requirements generation complete")
            return requirements
            
        except Exception as e:
            print(f"Error generating requirements: {str(e)}")
            return {
                "error": str(e),
                "status": "failed"
            }
