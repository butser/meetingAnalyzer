from setuptools import setup, find_packages

setup(
    name="meeting-analyzer",
    version="1.0.0",
    description="AI-powered meeting analyzer that processes video and audio to generate SRS documentation",
    author="Meeting Analyzer Team",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=1.0.0",
        "opencv-python>=4.8.0",
        "Pillow>=10.0.0",
        "SpeechRecognition>=3.10.0",
        "pydub>=0.25.0",
        "python-docx>=1.0.0",
        "markdown>=3.5.0",
        "tqdm>=4.66.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "meeting-analyzer=meeting_analyzer.cli:main",
        ],
    },
)
