def clean_text(text: str):
    """A generic text cleaning utility."""
    if not isinstance(text, str):
        return ""
    return text.strip().lower()
