"""
Pattern calculator for GitHub contribution graph
Converts text to grid coordinates
"""

from fonts import FONTS, UNKNOWN_CHAR

CHAR_WIDTH = 5  # Each character is 5 pixels wide
CHAR_HEIGHT = 7  # Each character is 7 pixels tall
CHAR_SPACING = 1  # 1 week spacing between characters
MAX_WEEKS = 53  # GitHub contribution graph is 53 weeks wide
MAX_DAYS = 7  # 7 days per week


def calculate_required_weeks(text):
    """Calculate how many weeks are needed for the given text"""
    if not text:
        return 0
    return (len(text) * (CHAR_WIDTH + CHAR_SPACING)) - CHAR_SPACING


def get_max_characters():
    """Calculate maximum characters that fit in the grid"""
    return (MAX_WEEKS + CHAR_SPACING) // (CHAR_WIDTH + CHAR_SPACING)


def validate_text(text):
    """Validate if text fits in the contribution graph"""
    if not text or not text.strip():
        return False, "Please enter some text"
    
    required = calculate_required_weeks(text)
    max_chars = get_max_characters()
    
    if required > MAX_WEEKS:
        return False, f"Text too long! Max {max_chars} chars (needs {required} weeks, max {MAX_WEEKS})"
    
    return True, "OK"


def text_to_pattern(text):
    """
    Convert text to pattern coordinates
    Returns list of (week, day, char) tuples
    """
    if not text:
        return []
    
    upper_text = text.upper()
    coordinates = []
    current_week = 0
    
    for char_index, char in enumerate(upper_text):
        font = FONTS.get(char, UNKNOWN_CHAR)
        
        # For each column in the character (5 columns wide)
        for col in range(CHAR_WIDTH):
            # For each row (7 rows tall, days 0-6)
            for row in range(CHAR_HEIGHT):
                if font[row][col] == 1:
                    coordinates.append({
                        'week': current_week + col,
                        'day': row,
                        'char': char,
                        'char_index': char_index
                    })
        
        # Move to next character position (width + spacing)
        current_week += CHAR_WIDTH + CHAR_SPACING
    
    return coordinates


def preview_pattern(text):
    """
    Generate a 2D preview array for visualization
    Returns 7 rows x calculated weeks columns
    """
    if not text:
        return []
    
    coordinates = text_to_pattern(text)
    required_weeks = calculate_required_weeks(text)
    
    # Create empty grid
    grid = [[0 for _ in range(required_weeks)] for _ in range(MAX_DAYS)]
    
    # Fill in the pattern
    for coord in coordinates:
        week, day = coord['week'], coord['day']
        if week < required_weeks and day < MAX_DAYS:
            grid[day][week] = 1
    
    return grid


def get_pattern_stats(text):
    """Get pattern statistics"""
    coordinates = text_to_pattern(text)
    required_weeks = calculate_required_weeks(text)
    max_chars = get_max_characters()
    
    return {
        'characters': len(text),
        'max_characters': max_chars,
        'commits': len(coordinates),
        'weeks': required_weeks,
        'max_weeks': MAX_WEEKS,
        'fits_in_graph': required_weeks <= MAX_WEEKS
    }
