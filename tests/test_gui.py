"""
Tests for GUI functionality
"""

import unittest
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meeting_analyzer.analyzer import MeetingAnalyzer


class TestGUIIntegration(unittest.TestCase):
    """Test GUI integration with analyzer"""
    
    def test_analyzer_accepts_progress_callback(self):
        """Test that analyzer accepts a progress callback"""
        # Track callback calls
        callback_calls = []
        
        def progress_callback(step, total_steps, message, error=None):
            callback_calls.append({
                'step': step,
                'total_steps': total_steps,
                'message': message,
                'error': error
            })
        
        # Create analyzer with callback
        analyzer = MeetingAnalyzer(
            video_path="test_video.mp4",
            progress_callback=progress_callback
        )
        
        # Verify callback is stored
        self.assertIsNotNone(analyzer.progress_callback)
        self.assertEqual(analyzer.progress_callback, progress_callback)
    
    def test_analyzer_without_progress_callback(self):
        """Test that analyzer works without a progress callback"""
        # Create analyzer without callback
        analyzer = MeetingAnalyzer(
            video_path="test_video.mp4"
        )
        
        # Verify callback is None
        self.assertIsNone(analyzer.progress_callback)
    
    def test_gui_imports_correctly(self):
        """Test that GUI module can be imported"""
        try:
            from meeting_analyzer.gui import MeetingAnalyzerGUI, main
            self.assertTrue(True, "GUI module imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import GUI module: {e}")
    
    def test_gui_has_required_methods(self):
        """Test that GUI class has all required methods"""
        from meeting_analyzer.gui import MeetingAnalyzerGUI
        
        required_methods = [
            'setup_ui',
            'browse_video',
            'browse_output',
            'start_analysis',
            'stop_analysis',
            'update_progress',
            'show_error',
            'analysis_complete',
            'open_file',
            'open_output_folder',
        ]
        
        for method_name in required_methods:
            self.assertTrue(
                hasattr(MeetingAnalyzerGUI, method_name),
                f"GUI class missing required method: {method_name}"
            )


if __name__ == '__main__':
    # Change to project root directory
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Run tests
    unittest.main(verbosity=2)
