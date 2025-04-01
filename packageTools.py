# packageTools.py
import json
import os
import zipfile
from typing import Any, Dict, List


def update_version(metadata_file: str, new_version: str, kicad_version: str = "8.0", status: str = "stable") -> None:
    """Update the latest version in the metadata file."""
    with open(metadata_file, "r", encoding="utf-8") as f:
        metadata: Dict[str, Any] = json.load(f)

    # Remove all existing versions and add new one
    metadata["versions"] = [{"version": new_version, "status": status, "kicad_version": kicad_version}]

    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)


def create_zip_archive(output_zip_file: str, files_and_dirs: List[str], min_size_bytes: int = 128) -> None:
    """Create a ZIP archive excluding files <= specified size in bytes."""
    with zipfile.ZipFile(output_zip_file, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zip_file:
        for path in files_and_dirs:
            if os.path.isdir(path):
                for root, _, files in os.walk(path):
                    for filename in files:
                        file_path = os.path.join(root, filename)
                        if _should_include(file_path, min_size_bytes):
                            rel_path = os.path.relpath(file_path, start=".")
                            zip_file.write(file_path, rel_path)
            elif _should_include(path, min_size_bytes):
                zip_file.write(path)


def _should_include(file_path: str, min_size: int) -> bool:
    """Helper to validate if a file should be included in the archive."""
    return os.path.isfile(file_path) and os.path.getsize(file_path) > min_size
