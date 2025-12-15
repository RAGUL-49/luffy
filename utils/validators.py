"""
Input Validators - Validate user inputs
"""
import re

def validate_input(word):
    """
    Validate user input word/name
    
    Args:
        word (str): Input word to validate
        
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    
    # Check if word exists
    if not word:
        return False, 'Word/name is required'
    
    # Convert to string and strip
    clean_word = str(word).strip()
    
    # Check if empty after stripping
    if len(clean_word) == 0:
        return False, 'Word/name cannot be empty'
    
    # Check length
    if len(clean_word) > 50:
        return False, 'Word/name must be 50 characters or less'
    
    if len(clean_word) < 2:
        return False, 'Word/name must be at least 2 characters'
    
    # Check for valid characters
    valid_pattern = re.compile(r"^[a-zA-Z0-9\s\-']+$")
    if not valid_pattern.match(clean_word):
        return False, "Word/name contains invalid characters. Use only letters, numbers, spaces, hyphens, and apostrophes"
    
    # Basic profanity check (expand as needed)
    profanity_list = ['test_bad_word']  # Add actual words if needed
    lower_word = clean_word.lower()
    
    for profane_word in profanity_list:
        if profane_word in lower_word:
            return False, 'Please use appropriate language'
    
    return True, clean_word

def validate_language(language):
    """
    Validate if language is supported
    
    Args:
        language (str): Language to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    supported_languages = [
        'English', 'Spanish', 'French', 'German', 'Italian',
        'Japanese', 'Korean', 'Chinese', 'Hindi', 'Tamil',
        'Portuguese', 'Arabic'
    ]
    return language in supported_languages