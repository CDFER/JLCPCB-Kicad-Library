# packageTools.py
import json
import os
import zipfile

def add_version(metadata_file, new_version, kicad_version = "8.0", status = "stable"):
    """Add a new version to the metadata file if it doesn't already exist."""
    with open(metadata_file, 'r') as f:
        metadata = json.load(f)

    if any(version['version'] == new_version for version in metadata['versions']):
        print(f"Version {new_version} already exists in metadata.json")
        return

    metadata['versions'].append({
        "version": new_version,
        "status": status,
        "kicad_version": kicad_version
    })

    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=4)

def create_zip_archive(output_zip_file, files_and_dirs):
    """Create a ZIP archive with the specified files and directories."""
    with zipfile.ZipFile(output_zip_file, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zip_file:
        for file_or_dir in files_and_dirs:
            if os.path.isdir(file_or_dir):
                for root, dirs, files in os.walk(file_or_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, start='.')
                        zip_file.write(file_path, rel_path)
            else:
                zip_file.write(file_or_dir)