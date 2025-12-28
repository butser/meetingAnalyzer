"""
Tests for hardware profile configuration
"""

import unittest
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meeting_analyzer.profiles import get_profile, list_profiles, get_profile_description, PROFILES


class TestProfiles(unittest.TestCase):
    """Test hardware profile functionality"""
    
    def test_profiles_exist(self):
        """Test that expected profiles are defined"""
        profiles = list_profiles()
        self.assertIn('laptop', profiles)
        self.assertIn('pc', profiles)
        self.assertEqual(len(profiles), 2)
    
    def test_laptop_profile_structure(self):
        """Test laptop profile has required fields"""
        profile = get_profile('laptop')
        
        # Check required fields
        self.assertIn('whisper_model', profile)
        self.assertIn('vision_model', profile)
        self.assertIn('text_model', profile)
        self.assertIn('vision_on_cpu', profile)
        self.assertIn('description', profile)
        
        # Check values
        self.assertEqual(profile['whisper_model'], 'small')
        self.assertEqual(profile['vision_on_cpu'], True)
        self.assertIsInstance(profile['description'], str)
    
    def test_pc_profile_structure(self):
        """Test PC profile has required fields"""
        profile = get_profile('pc')
        
        # Check required fields
        self.assertIn('whisper_model', profile)
        self.assertIn('vision_model', profile)
        self.assertIn('text_model', profile)
        self.assertIn('vision_on_cpu', profile)
        self.assertIn('description', profile)
        
        # Check values
        self.assertEqual(profile['whisper_model'], 'large-v3')
        self.assertEqual(profile['vision_on_cpu'], False)
        self.assertIsInstance(profile['description'], str)
    
    def test_get_invalid_profile(self):
        """Test that getting invalid profile raises ValueError"""
        with self.assertRaises(ValueError):
            get_profile('nonexistent')
    
    def test_get_profile_returns_copy(self):
        """Test that get_profile returns a copy, not original"""
        profile1 = get_profile('laptop')
        profile2 = get_profile('laptop')
        
        # Modify one copy
        profile1['whisper_model'] = 'modified'
        
        # Check that other copy is unchanged
        self.assertEqual(profile2['whisper_model'], 'small')
        
        # Check that original is unchanged
        self.assertEqual(PROFILES['laptop']['whisper_model'], 'small')
    
    def test_get_profile_description(self):
        """Test profile descriptions"""
        laptop_desc = get_profile_description('laptop')
        pc_desc = get_profile_description('pc')
        
        self.assertIn('GTX 1050 Ti', laptop_desc)
        self.assertIn('4GB VRAM', laptop_desc)
        self.assertIn('RTX 4090', pc_desc)
        self.assertIn('24GB VRAM', pc_desc)
    
    def test_get_invalid_profile_description(self):
        """Test description for invalid profile"""
        desc = get_profile_description('invalid')
        self.assertIn('Unknown profile', desc)
    
    def test_profile_models_are_strings(self):
        """Test that all model names are strings"""
        for profile_name in list_profiles():
            profile = get_profile(profile_name)
            self.assertIsInstance(profile['whisper_model'], str)
            self.assertIsInstance(profile['vision_model'], str)
            self.assertIsInstance(profile['text_model'], str)
    
    def test_profile_vision_on_cpu_is_bool(self):
        """Test that vision_on_cpu is boolean"""
        for profile_name in list_profiles():
            profile = get_profile(profile_name)
            self.assertIsInstance(profile['vision_on_cpu'], bool)


if __name__ == '__main__':
    # Change to project root directory
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Run tests
    unittest.main(verbosity=2)
