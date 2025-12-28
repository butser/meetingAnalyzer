"""
Basic structure tests for Meeting Analyzer
Tests that don't require external dependencies
"""

import unittest
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestStructure(unittest.TestCase):
    """Test basic module structure"""
    
    def test_package_exists(self):
        """Test that the meeting_analyzer package exists"""
        self.assertTrue(os.path.exists('meeting_analyzer'))
        self.assertTrue(os.path.isdir('meeting_analyzer'))
    
    def test_required_files_exist(self):
        """Test that required files are present"""
        required_files = [
            'meeting_analyzer/__init__.py',
            'meeting_analyzer/analyzer.py',
            'meeting_analyzer/video_processor.py',
            'meeting_analyzer/audio_processor.py',
            'meeting_analyzer/ai_analyzer.py',
            'meeting_analyzer/srs_generator.py',
            'meeting_analyzer/cli.py',
            'meeting_analyzer/profiles.py',
            'requirements.txt',
            'setup.py',
            'README.md',
            '.gitignore',
            '.env.example'
        ]
        
        for file_path in required_files:
            self.assertTrue(
                os.path.exists(file_path),
                f"Required file missing: {file_path}"
            )
    
    def test_python_files_compile(self):
        """Test that all Python files compile without syntax errors"""
        import py_compile
        
        python_files = [
            'meeting_analyzer/__init__.py',
            'meeting_analyzer/analyzer.py',
            'meeting_analyzer/video_processor.py',
            'meeting_analyzer/audio_processor.py',
            'meeting_analyzer/ai_analyzer.py',
            'meeting_analyzer/srs_generator.py',
            'meeting_analyzer/cli.py',
            'meeting_analyzer/profiles.py',
            'setup.py',
            'example_usage.py'
        ]
        
        for file_path in python_files:
            try:
                py_compile.compile(file_path, doraise=True)
            except py_compile.PyCompileError as e:
                self.fail(f"Syntax error in {file_path}: {e}")
    
    def test_requirements_file_format(self):
        """Test that requirements.txt has proper format"""
        with open('requirements.txt', 'r') as f:
            lines = f.readlines()
        
        # Should have at least some requirements
        self.assertGreater(len(lines), 5)
        
        # Check for expected dependencies (local AI providers + openai for LM Studio)
        content = ''.join(lines)
        expected_deps = ['faster-whisper', 'opencv-python', 'python-docx', 'openai']
        for dep in expected_deps:
            self.assertIn(dep, content, f"Expected dependency '{dep}' not found")
    
    def test_setup_file_structure(self):
        """Test that setup.py has proper structure"""
        with open('setup.py', 'r') as f:
            content = f.read()
        
        # Check for essential setup.py elements
        self.assertIn('setup(', content)
        self.assertIn('name=', content)
        self.assertIn('version=', content)
        self.assertIn('packages=', content)
    
    def test_gitignore_has_essentials(self):
        """Test that .gitignore includes essential patterns"""
        with open('.gitignore', 'r') as f:
            content = f.read()
        
        essential_patterns = [
            '__pycache__',
            '.env',
            '*.pyc',
            'venv'
        ]
        
        for pattern in essential_patterns:
            self.assertIn(pattern, content, f"Missing .gitignore pattern: {pattern}")
    
    def test_readme_has_content(self):
        """Test that README has substantial content"""
        with open('README.md', 'r') as f:
            content = f.read()
        
        # README should be substantial
        self.assertGreater(len(content), 1000, "README seems too short")
        
        # Should contain key sections
        self.assertIn('Installation', content)
        self.assertIn('Usage', content)
    
    def test_config_json_valid(self):
        """Test that config.json is valid JSON"""
        import json
        
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        # Should have expected structure
        self.assertIn('meeting_analyzer', config)
        self.assertIn('default_settings', config)


class TestModuleStructure(unittest.TestCase):
    """Test module structure without importing dependencies"""
    
    def test_module_docstrings(self):
        """Test that modules have docstrings"""
        modules = [
            'meeting_analyzer/analyzer.py',
            'meeting_analyzer/video_processor.py',
            'meeting_analyzer/audio_processor.py',
            'meeting_analyzer/ai_analyzer.py',
            'meeting_analyzer/srs_generator.py',
            'meeting_analyzer/cli.py'
        ]
        
        for module_path in modules:
            with open(module_path, 'r') as f:
                content = f.read()
            
            # Should start with a docstring
            self.assertTrue(
                content.strip().startswith('"""') or content.strip().startswith("'''"),
                f"Module {module_path} missing docstring"
            )
    
    def test_class_definitions(self):
        """Test that expected classes are defined"""
        expected_classes = {
            'meeting_analyzer/video_processor.py': 'VideoProcessor',
            'meeting_analyzer/audio_processor.py': 'AudioProcessor',
            'meeting_analyzer/ai_analyzer.py': 'AIAnalyzer',
            'meeting_analyzer/srs_generator.py': 'SRSGenerator',
            'meeting_analyzer/analyzer.py': 'MeetingAnalyzer'
        }
        
        for file_path, class_name in expected_classes.items():
            with open(file_path, 'r') as f:
                content = f.read()
            
            self.assertIn(
                f'class {class_name}',
                content,
                f"Class {class_name} not found in {file_path}"
            )


if __name__ == '__main__':
    # Change to project root directory
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Run tests
    unittest.main(verbosity=2)
