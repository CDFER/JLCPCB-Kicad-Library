# handmadeLibrarySymbols.py
import os
import pandas as pd
import re


def generate_property(property, value):
    str = f"""\t\t(property "{property}" "{value}"\n\t\t\t(at 0 0 0)\n\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t\t(hide yes)\n\t\t\t)\n\t\t)\n"""
    return str


def update_component_inplace(lcsc, libraryName, properties):
    filename = os.path.join("symbols", f"JLCPCB-{libraryName}.kicad_sym")
    with open(filename, "r") as file:
        lines = file.readlines()

    lcsc_found = False
    properties_found = {prop: False for prop in properties.keys()}

    for i, line in enumerate(lines):
        if lcsc_found == False:
            if f'(property "LCSC" "C{lcsc}"' in line:
                lcsc_found = True
                line_offset = 1
                # print(f"Found {lcsc} on line {i} of {filename}")
                # Work Upwards to find datasheet
                if "datasheet" in properties or "description" in properties:
                    while ("(symbol" not in lines[i - line_offset]) and (line_offset < 30):
                        if '(property "Datasheet"' in lines[i - line_offset] and "datasheet" in properties:
                            lines[i - line_offset] = f'		(property "Datasheet" "{properties["datasheet"]}"\n'
                            properties_found["datasheet"] = True
                        elif '(property "Description"' in lines[i - line_offset] and "description" in properties:
                            lines[i - line_offset] = f'		(property "Description" "{properties["description"]}"\n'
                            properties_found["description"] = True
                        line_offset += 1

        else:
            if '(property "ki_keywords"' in line:
                keywords_index = i

            elif "(property " in line:
                for prop, found in properties_found.items():
                    if f'(property "{prop.title()}"' in line:
                        if not found and prop != "datasheet" and prop != "description":
                            lines[i] = f'\t\t(property "{prop.title()}" "{properties[prop]}"\n'
                            properties_found[prop] = True

            elif "(symbol" in line:
                for prop, found in properties_found.items():
                    if not found and prop != "datasheet" and prop != "description":
                        lines.insert(keywords_index, generate_property(prop.title(), properties[prop]))
                break

    if lcsc_found == False:
        archived_symbol_path = os.path.join("Archived-Symbols-Footprints", "JLCPCB-Kicad-Symbols")
        archived_symbols_lcsc = [
            os.path.splitext(filename)[0]
            for filename in os.listdir(archived_symbol_path)
            if filename.endswith(".kicad_sym")
        ]
        if f"{lcsc}" in archived_symbols_lcsc:
            print(
                f"Error: C{lcsc} not found in library {filename} but it was found in the archive folder: {archived_symbol_path}"
            )
        else:
            print(f"Error: https://jlcpcb.com/parts/componentSearch?searchTxt=c{lcsc} not found in library {filename}")
        return False
    else:
        with open(filename, "w") as file:
            file.writelines(lines)
            return True


symbol_header_lines = """(kicad_symbol_lib
    (version 20231120)
    (generator "CDFER_Archive_Tool")
    (generator_version "0.0")
 """

symbol_footer_lines = """)
"""


def create_archived_symbol_file(symbol_start_line, symbol_end_line, lines, lcsc):
    archived_symbols_folder = os.path.join("Archived-Symbols-Footprints", "JLCPCB-Kicad-Symbols")
    archived_symbol_lines = lines[symbol_start_line:symbol_end_line]

    # Write archived symbol to file
    archived_filename = os.path.join(archived_symbols_folder, f"{lcsc}.kicad_sym")
    with open(archived_filename, "w") as archived_file:
        archived_file.writelines(symbol_header_lines)
        archived_file.writelines(archived_symbol_lines)
        archived_file.writelines(symbol_footer_lines)
    print(f"Archived symbol as: {archived_filename}")


def update_library_stock_inplace(libraryName):
    df = pd.read_csv("jlcpcb-components-basic-preferred.csv")
    filename = os.path.join("symbols", f"JLCPCB-{libraryName}.kicad_sym")
    with open(filename, "r") as file:
        lines = file.readlines()

    no_stock = False
    lcsc = 0
    symbol_start_line = 0

    for i, line in enumerate(lines):
        lines[i] = lines[i].replace("℃", "°C")
        if line.startswith("\t(") or line.startswith(")"):
            if no_stock == True:
                create_archived_symbol_file(symbol_start_line, i, lines, lcsc)
                lines[symbol_start_line:i] = [""] * (
                    i - symbol_start_line
                )  # Remove symbol from library by replacing lines with empty strings
                no_stock = False
            symbol_start_line = i

        elif '(property "LCSC" "C' in line:
            # print(f"LCSC Found on line {i} {line}")
            numbers = [int(num) for num in re.findall("\\d+", line)]
            lcsc = numbers[0]

            rows = df[df["lcsc"] == lcsc]
            if len(rows) == 0:
                no_stock = True
                print(f"Error: No Stock found for https://jlcpcb.com/partdetail/C{lcsc}")

        elif '(property "Stock"' in line and no_stock == True:
            lines[i] = f'		(property "Stock" "0"\n'

    with open(filename, "w") as file:
        file.writelines(lines)
        return
