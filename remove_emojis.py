#!/usr/bin/env python3
"""Script to remove emojis from all Python and Markdown files."""

import os

emoji_map = {
    '\U0001F393': '',      # graduation cap
    '\U0001F4CB': '',      # clipboard
    '\U0001F4DA': '',      # books
    '\U0001F3AF': '',      # target
    '\u2705': '[OK]',      # checkmark
    '\u274C': '[FAIL]',    # x mark
    '\u26A0\uFE0F': '[!]', # warning
    '\u26A0': '[!]',       # warning alt
    '\U0001F50D': '',      # magnifying glass
    '\U0001F389': '',      # party
    '\U0001F4DD': '',      # memo
    '\U0001F504': '',      # arrows
    '\U0001F4AA': '',      # muscle
    '\U0001F4A1': '',      # lightbulb
    '\U0001F4CA': '',      # chart
    '\U0001F5C2\uFE0F': '',# folder
    '\U0001F5C2': '',      # folder alt
    '\u270F\uFE0F': '',    # pencil
    '\u270F': '',          # pencil alt
    '\U0001F4D6': '',      # book
    '\U0001F9D1\u200D\U0001F3EB': '', # teacher
    '\U0001F9D1': '',      # person
    '\U0001F4BE': '',      # floppy
    '\U0001F527': '',      # wrench
    '\U0001F517': '',      # link
    '\U0001F680': '',      # rocket
    '\U0001F44B': '',      # wave
    '\U0001FA9E': '',      # mirror
    '\U0001F4C5': '',      # calendar
    '\U0001F4C2': '',      # folder open
    '\U0001F916': '',      # robot
    '\U0001F4CC': '',      # pin
    '\u2728': '',          # sparkles
    '\u2022': '-',         # bullet
    '\u2192': '->',        # arrow
    '\u2265': '>=',        # gte
    '\U0001F3EB': '',      # school
}

def clean_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        for emoji, replacement in emoji_map.items():
            content = content.replace(emoji, replacement)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f'Error: {filepath} - {e}')
        return False

if __name__ == '__main__':
    count = 0
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    for root, dirs, files in os.walk(base_dir):
        # Skip .git directory
        dirs[:] = [d for d in dirs if d != '.git']
        
        for file in files:
            if file.endswith(('.py', '.md')) and file != 'remove_emojis.py':
                filepath = os.path.join(root, file)
                if clean_file(filepath):
                    count += 1
                    print(f'Cleaned: {os.path.relpath(filepath, base_dir)}')
    
    print(f'\nTotal files cleaned: {count}')
