import sys
from pathlib import Path
import zipfile
import unicodedata
import os
import shutil


CATEGORIES = {
    "Audio": [".mp3", ".wav", ".flac", ".wma"],
    "Docs": [".docx", ".txt", ".pdf"],
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov"],
    "Archives": [".zip", ".tar", ".gz"],
    }

UNKNOWN_CATEGORY = "Other"

def normalize(filename):
    # Транслітерація кирилічних символів на латинську
    normalized_name = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('utf-8')
    # Заміна всіх символів, крім букв і цифр, на "_"
    normalized_name = ''.join(c if c.isalnum() else '_' for c in normalized_name)
    return normalized_name


def get_categories(file:Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"


def move_file(file: Path, category: str, root_dir: Path) -> None:
    target_dir = root_dir.joinpath(category)
    if not target_dir.exists():
        target_dir.mkdir(parents=True)
    new_filename = normalize(file.stem)
    new_path = target_dir.joinpath(new_filename + file.suffix)
    if not new_path.exists():
        file.replace(new_path)

def extract_archives(path: Path):
    for element in path.glob("**/*"):
        if element.is_file() and element.suffix.lower() in [".zip", ".tar", ".gz"]:
            with zipfile.ZipFile(element, 'r') as zip_ref:
                target_dir = path.joinpath("Archives", element.stem)
                target_dir.mkdir(parents=True, exist_ok=True)
                zip_ref.extractall(target_dir)
            element.unlink()


def sort_folder(path:Path) -> None:
    
    for element in path.glob("**/*"):
        if element.is_file():
            category = get_categories(element)
            move_file(element, category, path)

def remove_empty_folders(path: Path) -> None:
    for folder in path.glob("**/*"):
        if folder.is_dir() and not any(folder.glob("*")):
            folder.rmdir()


def main() -> str:
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"
    
    if not path.exists():
        return "Folder dos not exists"
    
    extract_archives(path)
    sort_folder(path)
    remove_empty_folders(path)
    
    return "All Ok"


if __name__ == '__main__':
    print(main())

    

