"""
Markdown utilities for rendering markdown content as HTML.
Supports Facebook-compatible markdown formatting.
"""

import re
from django.utils.safestring import mark_safe


def markdown_to_html(text):
    """
    Convert markdown text to HTML.
    Supports Facebook-compatible markdown formatting:
    - *text* or **text** = bold
    - _text_ or __text__ = italic
    - ~text~ = strikethrough
    - Line breaks are preserved
    
    Args:
        text (str): Markdown formatted text
        
    Returns:
        str: HTML formatted text (marked as safe for Django templates)
    """
    if not text:
        return ""
    
    # Escape HTML special characters first (but preserve newlines)
    text = escape_html(text)
    
    # Convert line breaks to <br> tags
    text = text.replace('\n', '<br>')
    
    # Convert **bold** to <strong>bold</strong>
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    
    # Convert *bold* to <strong>bold</strong> (single asterisks)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<strong>\1</strong>', text)
    
    # Convert __italic__ to <em>italic</em>
    text = re.sub(r'__(.+?)__', r'<em>\1</em>', text)
    
    # Convert _italic_ to <em>italic</em> (single underscores)
    text = re.sub(r'(?<!_)_(?!_)(.+?)(?<!_)_(?!_)', r'<em>\1</em>', text)
    
    # Convert ~strikethrough~ to <del>strikethrough</del>
    text = re.sub(r'~(.+?)~', r'<del>\1</del>', text)
    
    # Convert URLs to links
    text = convert_urls_to_links(text)
    
    return mark_safe(text)


def escape_html(text):
    """
    Escape HTML special characters while preserving newlines.
    
    Args:
        text (str): Text to escape
        
    Returns:
        str: Escaped text
    """
    replacements = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;',
    }
    
    for char, escape in replacements.items():
        text = text.replace(char, escape)
    
    return text


def convert_urls_to_links(text):
    """
    Convert URLs in text to clickable links.
    
    Args:
        text (str): Text containing URLs
        
    Returns:
        str: Text with URLs converted to links
    """
    # Match URLs starting with http:// or https://
    url_pattern = r'(https?://[^\s<>"{}|\\^`\[\]]*)'
    text = re.sub(url_pattern, r'<a href="\1" target="_blank">\1</a>', text)
    
    return text


def strip_markdown(text):
    """
    Remove markdown formatting from text, leaving only plain text.
    Useful for previews or plain text exports.
    
    Args:
        text (str): Markdown formatted text
        
    Returns:
        str: Plain text without markdown formatting
    """
    if not text:
        return ""
    
    # Remove bold formatting
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'\1', text)
    
    # Remove italic formatting
    text = re.sub(r'__(.+?)__', r'\1', text)
    text = re.sub(r'(?<!_)_(?!_)(.+?)(?<!_)_(?!_)', r'\1', text)
    
    # Remove strikethrough formatting
    text = re.sub(r'~(.+?)~', r'\1', text)
    
    return text

