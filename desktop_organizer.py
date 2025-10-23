#!/usr/bin/env python3
"""
Desktop Organizer for macOS
Automatically sorts files on Desktop into folders based on file types.
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict


FILE_CATEGORIES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico', '.tiff', '.webp', '.heic'],
    'PDFs': ['.pdf'],
    'Documents': ['.doc', '.docx', '.txt', '.rtf', '.odt', '.pages', '.tex', '.md', '.csv', '.xlsx', '.xls', '.ppt', '.pptx'],
    'Videos': ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.m4v'],
    'Music': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
    'Archives': ['.zip', '.tar', '.gz', '.rar', '.7z', '.bz2', '.xz'],
    'Others': []
}

IGNORED_FILES = {'.DS_Store', '.localized', 'desktop.ini'}


def get_desktop_path():
    """Get the Desktop path for the current user."""
    return Path.home() / 'Desktop'


def get_category(file_extension):
    """Determine which category a file belongs to based on its extension."""
    file_extension = file_extension.lower()
    
    for category, extensions in FILE_CATEGORIES.items():
        if file_extension in extensions:
            return category
    
    return 'Others'


def get_unique_filename(target_dir, filename):
    """
    Generate a unique filename if a file with the same name already exists.
    Adds numbers like (1), (2), etc.
    """
    target_path = target_dir / filename
    
    if not target_path.exists():
        return filename
    
    name_stem = Path(filename).stem
    extension = Path(filename).suffix
    counter = 1
    
    while True:
        new_filename = f"{name_stem}({counter}){extension}"
        new_path = target_dir / new_filename
        
        if not new_path.exists():
            return new_filename
        
        counter += 1


def organize_desktop():
    """Main function to organize desktop files into categorized folders."""
    desktop_path = get_desktop_path()
    
    if not desktop_path.exists():
        print(f"Error: Desktop path not found at {desktop_path}")
        return
    
    print(f"Organizing files in: {desktop_path}\n")
    
    move_count = defaultdict(int)
    
    items = list(desktop_path.iterdir())
    
    for item in items:
        if not item.is_file():
            continue
        
        if item.name in IGNORED_FILES:
            continue
        
        if item.name.startswith('.'):
            continue
        
        file_extension = item.suffix
        category = get_category(file_extension)
        
        category_folder = desktop_path / category
        category_folder.mkdir(exist_ok=True)
        
        unique_filename = get_unique_filename(category_folder, item.name)
        destination = category_folder / unique_filename
        
        try:
            shutil.move(str(item), str(destination))
            move_count[category] += 1
            print(f"Moved: {item.name} → {category}/{unique_filename}")
        except Exception as e:
            print(f"Error moving {item.name}: {e}")
    
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    
    total_files = sum(move_count.values())
    
    if total_files == 0:
        print("No files were moved. Desktop is already organized or empty.")
    else:
        for category in sorted(move_count.keys()):
            count = move_count[category]
            print(f"{category}: {count} file{'s' if count != 1 else ''}")
        
        print(f"\nTotal files organized: {total_files}")


if __name__ == "__main__":
    organize_desktop()

