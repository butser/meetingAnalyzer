"""
Hardware profile configuration for Meeting Analyzer
"""

PROFILES = {
    "laptop": {
        "whisper_model": "small",
        "vision_model": "llava-v1.6-mistral-7b",  # LM Studio model name
        "text_model": "phi-3-mini-4k-instruct",
        "vision_on_cpu": True,
        "description": "GTX 1050 Ti (4GB VRAM), 48GB RAM"
    },
    "pc": {
        "whisper_model": "large-v3",
        "vision_model": "llava-v1.6-34b",
        "text_model": "llama-3.1-70b-instruct",
        "vision_on_cpu": False,
        "description": "RTX 4090 (24GB VRAM), 96GB RAM"
    }
}


def get_profile(profile_name: str) -> dict:
    """
    Get profile settings by name
    
    Args:
        profile_name: Name of the profile (laptop, pc)
        
    Returns:
        Dictionary with profile settings
        
    Raises:
        ValueError: If profile name is not recognized
    """
    if profile_name not in PROFILES:
        raise ValueError(
            f"Unknown profile: {profile_name}. "
            f"Available profiles: {', '.join(PROFILES.keys())}"
        )
    return PROFILES[profile_name].copy()


def list_profiles() -> list:
    """
    List all available profiles
    
    Returns:
        List of profile names
    """
    return list(PROFILES.keys())


def get_profile_description(profile_name: str) -> str:
    """
    Get human-readable description of a profile
    
    Args:
        profile_name: Name of the profile
        
    Returns:
        Description string
    """
    if profile_name not in PROFILES:
        return f"Unknown profile: {profile_name}"
    return PROFILES[profile_name].get("description", "No description")
