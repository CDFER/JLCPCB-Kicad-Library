import json
import math
import os
import re
import tempfile
from pathlib import Path
from typing import Iterable


REQUIRED_GENERATED_LIBRARIES = (
    "Resistors",
    "Capacitors",
    "Diodes",
    "Transistors",
    "Inductors",
)

THIRD_PARTY_VARIABLE = re.compile(r"\$\{KICAD\d+_3RD_PARTY\}")

FOOTPRINT_REFERENCE_REPLACEMENTS = {
    "PCM_JLCPCB:Q_SOT-89-3L": "PCM_JLCPCB:Q_SOT-89",
    "PCM_JLCPCB:D_DO-214AA(SMB)": "PCM_JLCPCB:D_SMB",
    "PCM_JLCPCB:D_P600": "Diode_THT:D_P600_R-6_P15.24mm_Horizontal",
}


def parse_base_price(value):
    """Return the first quantity-tier price from legacy JSON or current CSV text."""
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None

    text = str(value).strip()
    if not text:
        return None

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        parsed = None

    if isinstance(parsed, list) and parsed:
        price = parsed[0].get("price")
        return float(price) if price not in (None, "") else None

    first_tier = text.split(",", 1)[0]
    if ":" in first_tier:
        _, price = first_tier.rsplit(":", 1)
        try:
            return float(price)
        except ValueError:
            return None

    return None


def source_catalog_complete(categories: Iterable[str]) -> bool:
    present = {str(category) for category in categories if category}
    return all(name in present for name in REQUIRED_GENERATED_LIBRARIES)


def parse_attributes(value) -> dict:
    """Read attributes from both the legacy ``extra`` and current CSV schema."""
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return {}
    if isinstance(value, dict):
        data = value
    else:
        try:
            data = json.loads(str(value))
        except (json.JSONDecodeError, TypeError):
            return {}
    if not isinstance(data, dict):
        return {}
    nested = data.get("attributes")
    attributes = nested if isinstance(nested, dict) else data
    return {key: value for key, value in attributes.items() if value != "-"}


def atomic_write_text(path: os.PathLike | str, content: str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="") as temporary:
            temporary.write(content)
            temporary.flush()
            os.fsync(temporary.fileno())
        os.replace(temporary_name, target)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def rewrite_third_party_variable(content: str, kicad_version: str) -> str:
    major = kicad_version.split(".", 1)[0]
    return THIRD_PARTY_VARIABLE.sub(f"${{KICAD{major}_3RD_PARTY}}", content)


def rewrite_footprint_references(content: str) -> str:
    for old, new in FOOTPRINT_REFERENCE_REPLACEMENTS.items():
        content = content.replace(old, new)
    return content
