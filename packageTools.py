# packageTools.py
import json
import os
import zipfile
from pathlib import Path
from typing import Any, Dict, List

from build_support import rewrite_footprint_references, rewrite_third_party_variable


def update_version(metadata_file: str, new_version: str, kicad_version: str = "8.0", status: str = "stable") -> None:
    """Update the latest version in the metadata file."""
    with open(metadata_file, "r", encoding="utf-8") as f:
        metadata: Dict[str, Any] = json.load(f)

    # Remove all existing versions and add new one
    metadata["versions"] = [{"version": new_version, "status": status, "kicad_version": kicad_version}]

    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)


def create_zip_archive(
    output_zip_file: str,
    files_and_dirs: List[str],
    min_size_bytes: int = 0,
    *,
    root: str | os.PathLike = ".",
    package_version: str | None = None,
    kicad_version: str | None = None,
) -> None:
    """Create a PCM archive, optionally targeting one KiCad major release."""
    root_path = Path(root)
    with zipfile.ZipFile(output_zip_file, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zip_file:
        for path in files_and_dirs:
            source_path = root_path / path
            if source_path.is_dir():
                for current_root, _, files in os.walk(source_path):
                    for filename in files:
                        file_path = Path(current_root) / filename
                        if _should_include(file_path, min_size_bytes):
                            rel_path = file_path.relative_to(root_path).as_posix()
                            _write_package_file(
                                zip_file, file_path, rel_path, package_version=package_version, kicad_version=kicad_version
                            )
            elif _should_include(source_path, min_size_bytes):
                _write_package_file(
                    zip_file,
                    source_path,
                    source_path.relative_to(root_path).as_posix(),
                    package_version=package_version,
                    kicad_version=kicad_version,
                )


def _should_include(file_path: str, min_size: int) -> bool:
    """Helper to validate if a file should be included in the archive."""
    return os.path.isfile(file_path) and os.path.getsize(file_path) > min_size


def _write_package_file(zip_file, file_path, archive_path, *, package_version=None, kicad_version=None):
    if archive_path == "metadata.json" and package_version and kicad_version:
        metadata = json.loads(Path(file_path).read_text(encoding="utf-8"))
        version = {"version": package_version, "status": "stable", "kicad_version": kicad_version}
        if kicad_version != "10.0":
            version["kicad_version_max"] = f"{kicad_version.split('.', 1)[0]}.99"
        metadata["versions"] = [version]
        zip_file.writestr(archive_path, json.dumps(metadata, indent=4).encode("utf-8"))
    elif str(file_path).endswith(".kicad_mod") and kicad_version:
        content = Path(file_path).read_text(encoding="utf-8")
        zip_file.writestr(archive_path, rewrite_third_party_variable(content, kicad_version).encode("utf-8"))
    elif str(file_path).endswith(".kicad_sym"):
        content = Path(file_path).read_text(encoding="utf-8")
        zip_file.writestr(archive_path, rewrite_footprint_references(content).encode("utf-8"))
    else:
        zip_file.write(file_path, archive_path)


def create_target_archives(
    package_version: str,
    files_and_dirs: List[str],
    *,
    root: str | os.PathLike = ".",
    output_dir: str | os.PathLike = ".",
    kicad_versions=("8.0", "9.0", "10.0"),
) -> list[Path]:
    output_root = Path(output_dir)
    output_root.mkdir(parents=True, exist_ok=True)
    archives = []
    for kicad_version in kicad_versions:
        major = kicad_version.split(".", 1)[0]
        archive = output_root / f"JLCPCB-KiCad-Library-{package_version}-kicad{major}.zip"
        create_zip_archive(
            archive,
            files_and_dirs,
            root=root,
            package_version=package_version,
            kicad_version=kicad_version,
        )
        archives.append(archive)
    return archives
