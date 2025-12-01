"""
file_tools.py
==============
Simple utilities for saving stuff to files.
Study plans get saved as markdown, notes too.
Nothing fancy here, just making sure students can export their work.
"""

import os
import json
from datetime import datetime
from typing import Any, Dict

from config.settings import OUTPUT_DIR, STUDY_PLANS_DIR


def save_study_plan_to_file(filename: str, content: str) -> str:
    """
    Saves a study plan to a markdown file. Pretty straightforward -
    just dumps the content to output/study_plans/whatever.md
    """
    try:
        os.makedirs(STUDY_PLANS_DIR, exist_ok=True)
        
        # Ensure .md extension
        if not filename.endswith('.md'):
            filename = f"{filename}.md"
        
        filepath = os.path.join(STUDY_PLANS_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        return f"Study plan saved successfully to {filepath}"
    except Exception as e:
        return f"Error saving study plan: {str(e)}"


def save_notes_to_file(content: str, filename: str = "study_notes.md") -> str:
    """
    Save study notes to a file.
    
    Args:
        content: The notes content
        filename: Name of the file
    
    Returns:
        Success/failure message
    """
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        return f"Notes saved to {filepath}"
    except Exception as e:
        return f"Error saving notes: {str(e)}"


def export_flashcards(topic: str, flashcards: list, format: str = "md") -> str:
    """
    Export flashcards to a file for external use.
    
    Args:
        topic: The topic name
        flashcards: List of Q/A pairs
        format: Output format ('md' or 'json')
    
    Returns:
        Success/failure message
    """
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        safe_topic = topic.replace(" ", "_").lower()
        
        if format == "json":
            filename = f"flashcards_{safe_topic}.json"
            filepath = os.path.join(OUTPUT_DIR, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump({
                    "topic": topic,
                    "created": datetime.now().isoformat(),
                    "flashcards": flashcards
                }, f, indent=2)
        else:
            filename = f"flashcards_{safe_topic}.md"
            filepath = os.path.join(OUTPUT_DIR, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"# Flashcards: {topic}\n\n")
                f.write(f"*Created: {datetime.now().strftime('%Y-%m-%d')}*\n\n")
                for i, card in enumerate(flashcards, 1):
                    f.write(f"## Card {i}\n\n")
                    f.write(f"**Q:** {card.get('question', card.get('q', ''))}\n\n")
                    f.write(f"**A:** {card.get('answer', card.get('a', ''))}\n\n")
                    f.write("---\n\n")
        
        return f"Flashcards exported to {filepath}"
    except Exception as e:
        return f"Error exporting flashcards: {str(e)}"
