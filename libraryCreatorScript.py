import requests
import os
import json
import re
import shutil
import pandas as pd
from autoLibrarySymbols import *  # librarySymbols.py
from handmadeLibrarySymbols import *  # handmadeLibrarySymbols.py
from packageTools import * # packageTools.py
from datetime import datetime
from datetime import timezone


def download_file(url, filename):
    """
    Downloads a file from the specified URL and saves it to the given filename.
    If the file already exists, it will be deleted before downloading the new file.

    :param url: The base URL of the file to download.
    :param filename: The local filename to save the downloaded file.
    """
    try:
        # Check if the file already exists and delete it if it does
        if os.path.exists(filename):
            os.remove(filename)
            print(f"Deleted existing file: {filename}")

        # Construct the full URL for the file
        full_url = f"{url}/{filename}"

        # Send a GET request to download the file
        response = requests.get(full_url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Write the content to a file in binary mode
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=None):
                f.write(chunk)

        print(f"Downloaded {full_url} to {filename}")
    except requests.RequestException as e:
        print(f"Download failed for {full_url}: {e}")


def extract_capacitor_value(description, lcsc_id):
    """
    Extracts the capacitor value from the given description based on the LCSC ID.
    If the LCSC ID matches a known value, it returns the corresponding capacitance.
    Otherwise, it uses a regex pattern to extract the capacitance from the description.

    :param description: The description of the capacitor.
    :param lcsc_id: The LCSC ID of the capacitor.
    :return: The extracted capacitance value as a string, or None if no value is found.
    """
    # Define known LCSC IDs and their corresponding capacitance values
    known_values = {30274: "6pF", 3013473: "100nF", 3008298: "4.7nF"}

    # Check if the LCSC ID matches a known value
    if lcsc_id in known_values:
        return known_values[lcsc_id]

    # Define a regex pattern to match capacitance values
    pattern = r"(\d+(?:\.\d+)?(?:[pnu]?)(?:f|farad))"  # matches numbers followed by F, f, Farad, farad, pF, pf, nF, nf, uF, uf

    # Search for the pattern in the description
    match = re.search(pattern, description, re.IGNORECASE)
    if match:
        return match.group(0)
    else:
        print(f"Error: No value found for https://jlcpcb.com/partdetail/C{lcsc_id}  ({description})")
        return None


def extract_resistance_value(description, lcsc_id):
    """
    Extracts the resistance value from the given description based on the LCSC ID.
    If the LCSC ID matches a known value, it returns the corresponding resistance.
    Otherwise, it uses a regex pattern to extract the resistance from the description.

    :param description: The description of the resistor.
    :param lcsc_id: The LCSC ID of the resistor.
    :return: The extracted resistance value as a string, or None if no value is found.
    """
    # Define known LCSC IDs and their corresponding resistance values
    known_values = {22818: "16kΩ"}

    # Check if the LCSC ID matches a known value
    if lcsc_id in known_values:
        return known_values[lcsc_id]

    # Define a regex pattern to match resistance values
    pattern = r"(\d+(?:\.\d+)?(?:[kMGT]?)(?:Ω|ohm))"  # matches numbers followed by Ω, ohm, Ohm, or OHM

    # Search for the pattern in the description
    match = re.search(pattern, description, re.IGNORECASE)
    if match:
        return match.group(0)
    else:
        print(f"Error: No value found for https://jlcpcb.com/partdetail/C{lcsc_id}  ({description})")
        return None


def extract_diode_type(description, pins, lcsc_id):
    if lcsc_id == 2990493:
        return "TVS-Bi"
    if lcsc_id == 2990473:
        return "TVS-Bi"
    if lcsc_id == 2990416:
        return "TVS-Bi"
    if lcsc_id == 2990414:
        return "TVS-Bi"
    if lcsc_id == 2990261:
        return "TVS-Bi"
    if lcsc_id == 2990124:
        return "TVS-Bi"
    if lcsc_id == 3019524:
        return "TVS-Bi"
    if lcsc_id == 1323289:
        return "TVS-Bi"
    if lcsc_id == 3001945:
        return "TVS-Uni"
    if lcsc_id == 2833277:
        return "TVS-Bi"
    if lcsc_id == 2975471:
        return "TVS-Uni"
    if lcsc_id == 78395:
        return "TVS-Bi"
    if lcsc_id == 2925443:
        return "TVS-Uni"
    if lcsc_id == 2936988:
        return "TVS-Bi"
    if lcsc_id == 2925441:
        return "TVS-Bi"
    if lcsc_id == 2925451:
        return "TVS-Bi"
    if lcsc_id == 20617908:
        return "TVS-Bi"
    if lcsc_id == 20617910:
        return "TVS-Bi"
    if lcsc_id == 22466368:
        return "Schottky13"
    if lcsc_id == 22466371:
        return "Schottky13"
    if lcsc_id == 28646292:
        return "Schottky"
    if lcsc_id == 28646296:
        return "Schottky"
    if lcsc_id == 28646302:
        return "Schottky"
    if lcsc_id == 28646299:
        return "Schottky"
    if lcsc_id == 28646283:
        return "Schottky"
    if lcsc_id == 41411783:
        return "TVS-Uni"
    if lcsc_id == 41376087:
        return "TVS-Uni"

    diode_types = {
        "Schottky": {"pins": 2, "type": "Schottky"},
        "Recovery": {"pins": 2, "type": "Recovery"},
        "General": {"pins": 2, "type": "General"},
        "Switching": {"pins": 2, "type": "Switching"},
        "Zener": {"pins": 2, "type": "Zener"},
        "Bidirectional": {"pins": 2, "type": "TVS-Bi"},
        "Unidirectional": {"pins": 2, "type": "TVS-Uni"},
    }
    for keyword, diode_info in diode_types.items():
        if keyword.casefold() in description.casefold():
            if diode_info["pins"] == pins:
                return diode_info["type"]
            elif keyword == "Zener" and pins == 3:
                return "Zener13"
            else:
                return None
    return None


def extract_transistor_type(description, pins, footprint, lcsc_id):
    if lcsc_id == 484513:
        return "NMOS"
    if lcsc_id == 396043:
        return "NMOS"
    if lcsc_id == 916398:
        return "NMOS"
    if lcsc_id == 296127:
        return None
    if lcsc_id == 41375139:
        return "PNPC2"
    if lcsc_id == 28646267:
        return "NPNC2"

    transistor_types = {
        "PNP": {"pins": 3, "type": "PNP"},
        "NPN": {"pins": 3, "type": "NPN"},
        "NChannel": {"pins": 3, "type": "NMOS"},
        "PChannel": {"pins": 3, "type": "PMOS"},
        "N-Channel": {"pins": 3, "type": "NMOS"},
        "P-Channel": {"pins": 3, "type": "PMOS"},
    }
    for keyword, transistor_info in transistor_types.items():
        if keyword.casefold() in description.casefold():
            if transistor_info["pins"] == pins:
                if footprint == "SOT-89":
                    return f"{transistor_info["type"]}C2"  # Collector/ and Emitter pin number is flipped
                else:
                    return transistor_info["type"]
            else:
                # print(f"Error: Number of pins ({pins}) does not match expected ({transistor_info['pins']}) for https://jlcpcb.com/partdetail/C{lcsc_id}  ({description})")
                return None
    # print(f"Error: No transistor type found for https://jlcpcb.com/partdetail/C{lcsc_id}  ({description})")
    return None


def extract_LED_value(description, lcsc_):
    if lcsc == 2985996:
        return "Red", "LED"
    elif lcsc == 34499:
        return "White", "LED"
    elif lcsc == 2986058:
        return "Blue", "LED"
    elif lcsc == 2986059:
        return "Green", "LED"

    color_pattern = r"(Red|Green|Blue|Yellow|White|Emerald)"

    color_match = re.search(color_pattern, description, re.IGNORECASE)

    if color_match:
        color = color_match.group(0).replace("Emerald", "Green")
        return color, "LED"
    else:
        print(f"Error: No LED value extracted for https://jlcpcb.com/partdetail/C{lcsc}  ({description})")
        return None, None


def extract_inductor_type_value(description, joints, lcsc):
    current = None
    if lcsc == 2827387:
        current = "300mA"
    if lcsc == 2827415:
        current = "900mA"
    if lcsc == 3007708:
        current = "410mA"
    if lcsc == 2844914:
        current = "305mA"
    if lcsc == 2827354:
        current = "5.5A"
    if lcsc == 2827458:
        current = "400mA"
    if lcsc == 2835403:
        return "120nH,80mA", "Inductor"

    # Define patterns to match inductance values
    inductance_patterns = [
        r"\b(\d+\.\d+[u|m|n]H)\b",  # e.g. 10.5uH, 10.5mH, 10.5nH
        r"\b(\d+[u|m|n]H)\b",  # e.g. 10uH, 10mH, 10nH
    ]

    # Define patterns to match current values
    current_patterns = [
        r"(\d+(\.\d+)?)A",  # e.g. 1A, 2A, 4.95A
        r"(\d+)mA",  # e.g. 100mA, 2000mA
    ]

    # Iterate over patterns and search for matches
    for pattern in inductance_patterns:
        inductance_match = re.search(pattern, description, re.IGNORECASE)
        if inductance_match:
            # Extract inductance value
            inductance = inductance_match.group(1)

            # Extract current value
            if current == None:
                for current_pattern in current_patterns:
                    current_match = re.search(current_pattern, description, re.IGNORECASE)
                    if current_match:
                        current = current_match.group(1)
                        if "mA" in current_pattern:
                            current += "mA"
                        else:
                            current += "A"
                        break
                else:
                    current = ""
                    print(
                        f"Error: No current value extracted for https://jlcpcb.com/partdetail/C{lcsc}  ({description})"
                    )

            # Return inductance and current values
            return f"{inductance},{current}", "Inductor"

    if "Ferrite" in description:
        return "", "Ferrite"

    # If no match is found, print an error message and return None
    print(f"Error: No inductance value extracted for https://jlcpcb.com/partdetail/C{lcsc}  ({description})")
    return None, None


def extract_variable_resistor_type_value(description, lcsc):
    # NTC Thermistors
    if lcsc == 2991699:
        return "NTC", "47kΩ,4050"
    if "NTC" in description:
        pattern = r"(\d+(?:\.\d+)?Ω)"  # matches numbers followed by Ω
        match = re.search(pattern, description)
        if match:
            return "NTC", match.group(0)
        else:
            print(f"Error: Unknown resistance for https://jlcpcb.com/partdetail/C{lcsc}  ({description})")
            return None, None

    # Varistors (MOV)
    elif "Varistors" in description:
        return "MOV", ""

    # Fuses
    elif "Fuse" or "fuse" in description:
        if lcsc == 2924957:
            value = "1.5A"
        elif lcsc == 2838983:
            value = "1.5A"
        else:
            value = ""
        if "Resettable" in description:
            return "Fuse,Resettable", value
        else:
            return "Fuse", value

    # Unknown
    else:
        print(f"Error: Unknown type for https://jlcpcb.com/partdetail/C{lcsc}  ({description})")
        return None, None


def extract_capacitor_voltage(description, lcsc):
    voltage_pattern = r"\b(\d+(?:\.\d+)?)(V|kV)\b"
    voltage_match = re.search(voltage_pattern, description, re.IGNORECASE)

    if voltage_match:
        return voltage_match.group(0)
    else:
        return None


def get_basic_or_prefered_type(df, index):
    if df.loc[index, "basic"] > 0:
        return "Basic Component"
    elif df.loc[index, "preferred"] > 0:
        return "Preferred Component"
    else:
        print("extended component found")
        return "Extended Component"


def generate_kicad_symbol_libs(symbols):
    for lib_name, symbol_list in symbols.items():
        lib_content = "(kicad_symbol_lib\n"
        lib_content += "\t(version 20231120)\n"
        lib_content += '\t(generator "CDFER")\n'
        lib_content += '\t(generator_version "8.0")\n'
        for symbol in symbol_list:
            lib_content += symbol + "\n"
        lib_content += ")\n"

        lib_content = lib_content.replace("℃", "°C")

        with open(f"symbols/JLCPCB-{lib_name}.kicad_sym", "w") as f: #TODO switch with OS.join
            f.write(lib_content)


def check_models():
    exempt_footprints = [
        "Hole, 3mm",
        "Hole_Tooling_JLCPCB",
        "MouseBites, Cosmetic, JLCPCB, 1.6mm",
        "MouseBites, Mechanical, JLCPCB, 1.6mm",
        "Part_Num_JLCPCB",
    ]

    footprints_folder_path = os.path.join("footprints", "JLCPCB.pretty")
    models_folder_path = os.path.join("3dmodels", "JLCPCB.3dshapes")
    archived_models_folder_path = os.path.join("Archived-Symbols-Footprints", "JLCPCB-Kicad-Footprints", "3dModels")

    footprint_names = [
        os.path.splitext(filename)[0]
        for filename in os.listdir(footprints_folder_path)
        if filename.endswith(".kicad_mod")
    ]
    archived_model_names = [
        os.path.splitext(filename)[0]
        for filename in os.listdir(archived_models_folder_path)
        if filename.endswith(".step")
    ]
    model_names = [
        os.path.splitext(filename)[0] for filename in os.listdir(models_folder_path) if filename.endswith(".step")
    ]

    model_names_used = []

    for footprint_name in footprint_names:
        footprint_file_path = os.path.join(footprints_folder_path, f"{footprint_name}.kicad_mod")

        with open(footprint_file_path, "r") as file:
            content = file.read()
            match = re.search(r'\(model "([^"]+)"', content)

            if match:
                model_path = match.group(1)
                model = re.search(r'${KICAD8_3RD_PARTY}/3dmodels/com_github_CDFER_JLCPCB-Kicad-Library/JLCPCB.3dshapes/([^"]+).step', model_path)
                if model:
                    model = model.group(1)
                    if model not in model_names:
                        if model in archived_model_names:
                            post_move_file_path = os.path.join(models_folder_path, f"{model}.step")
                            pre_move_file_path = os.path.join(archived_models_folder_path, f"{model}.step")
                            shutil.move(pre_move_file_path, post_move_file_path)
                            archived_model_names.remove(model)
                            print(f"Un-archived needed model: {model}")
                        else:
                            print(f"Missing 3D Model for Footprint: {footprint_name} ({model_path})")
                    else:
                        model_names_used.append(model)
                else:
                    print(f"Incorrect Model path for Footprint: {footprint_name} ({model_path})")
            elif footprint_name not in exempt_footprints:
                print(f"Empty Model Field for Footprint: {footprint_name}")

    for model in model_names:
        if model not in model_names_used:
            pre_move_file_path = os.path.join(models_folder_path, f"{model}.step")
            post_move_file_path = os.path.join(archived_models_folder_path, f"{model}.step")
            shutil.move(pre_move_file_path, post_move_file_path)
            print(f"Archived unused model: {model}")


def check_footprints():
    symbols_folder_path = "symbols"
    footprints_folder_path = os.path.join("footprints", "JLCPCB.pretty")
    archived_footprints_folder_path = os.path.join("Archived-Symbols-Footprints", "JLCPCB-Kicad-Footprints")

    archived_footprint_names = [
        os.path.splitext(filename)[0]
        for filename in os.listdir(archived_footprints_folder_path)
        if filename.endswith(".kicad_mod")
    ]
    footprint_names = [
        os.path.splitext(filename)[0]
        for filename in os.listdir(footprints_folder_path)
        if filename.endswith(".kicad_mod")
    ]
    footprint_names_used = []

    for symbol_lib_filename in os.listdir(symbols_folder_path):
        footprint_file_path = os.path.join(symbols_folder_path, symbol_lib_filename)

        if os.path.isfile(footprint_file_path) and symbol_lib_filename.endswith(".kicad_sym"):
            with open(footprint_file_path, "r") as file:
                symbol_name = None
                footprint_name = None

                for line in file:
                    # Search for symbol name
                    match = re.search(r'\(symbol "([^"]+)"', line)
                    if match:
                        symbol_name = match.group(1)
                        footprint_name = None

                    # Search for footprint
                    match = re.search(r'\(property "Footprint" "([^"]+)"', line)
                    if match:
                        footprint_name = match.group(1)
                        footprint_lib_match = re.search(r'PCM_JLCPCB:([^"]+)', footprint_name)
                        if footprint_lib_match:
                            footprint_name = footprint_lib_match.group(1)
                            if footprint_name not in footprint_names:
                                if footprint_name in archived_footprint_names:
                                    post_move_file_path = os.path.join(
                                        footprints_folder_path, f"{footprint_name}.kicad_mod"
                                    )
                                    pre_move_file_path = os.path.join(
                                        archived_footprints_folder_path, f"{footprint_name}.kicad_mod"
                                    )
                                    shutil.move(pre_move_file_path, post_move_file_path)
                                    archived_footprint_names.remove(footprint_name)
                                    print(f"Un-archived needed footprint: {footprint_name}")
                                else:
                                    print(
                                        f"Missing Footprint For Symbol: {symbol_name} -> {footprint_name} ({footprint_file_path})"
                                    )
                            else:
                                footprint_names_used.append(footprint_name)
                        else:
                            print(
                                f"Incorrect Symbol Footprint Library For Symbol: {symbol_name} -> {footprint_name} ({footprint_file_path})"
                            )

    for footprint in footprint_names:
        if footprint not in footprint_names_used:
            pre_move_file_path = os.path.join(footprints_folder_path, f"{footprint}.kicad_mod")
            post_move_file_path = os.path.join(archived_footprints_folder_path, f"{footprint}.kicad_mod")
            shutil.move(pre_move_file_path, post_move_file_path)
            print(f"Archived unused footprint: {footprint}")


# Download the latest basic/preferred csv file
download_file("https://cdfer.github.io/jlcpcb-parts-database", "jlcpcb-components-basic-preferred.csv")

df = pd.read_csv("jlcpcb-components-basic-preferred.csv")

footprints_dir = "3dmodels/JLCPCB.3dshapes"
footprints_lookup = {os.path.splitext(file)[0] for file in os.listdir(footprints_dir)}

symbols = {
    "Resistors": [],
    "Capacitors": [],
    "Diodes": [],
    "Transistors": [],
    "Inductors": [],
    "Variable-Resistors": [],
}
smt_joint_cost = 0.0017
hand_solder_joint_cost = 0.0173

componentList = []
names_lookup = []

for index in range(0, len(df)):
    # lcsc,category_id,category,subcategory,mfr,package,joints,manufacturer,basic,preferred,description,datasheet,stock,last_on_stock,price,extra
    lcsc = int(df.loc[index, "lcsc"])
    category = f'{df.loc[index,"category"]},{df.loc[index,"subcategory"]}'
    manufacturer = str(df.loc[index, "manufacturer"])
    manufacturerPartID = df.loc[index, "mfr"]
    footprint_name = str(df.loc[index, "package"])
    footprint_name = footprint_name.replace("插件","Plugin") # Some through-hole parts use the prefix Plugin or the chinese equivalent
    description = str(df.loc[index, "description"])
    description = description.replace("  ", " ") # Gets rid of double spaces
    joints = int(df.loc[index, "joints"])
    assembly_process = df.loc[index, "Assembly Process"]
    min_order_qty = int(df.loc[index, "Min Order Qty"])
    attrition_qty = int(df.loc[index, "Attrition Qty"])
    units = 1
    secondary_mode = ""
    subcategory = str(df.loc[index, "subcategory"])
    
    if assembly_process == "THT":
        assembly_process = "Hand-Soldered"
        joint_cost = hand_solder_joint_cost
    else:
        joint_cost = smt_joint_cost

    try:
        price_json = json.loads(df.loc[index, "price"])
        if price_json and len(price_json) > 0 and "price" in price_json[0]:
            base_price = float(price_json[0]["price"])
            # Calculate the total price considering joints and joint cost
            price = base_price + (joints * joint_cost)
            price = round(price, 3)
            price_str = f"{price:.3f}USD"

        else:
            price_str = f""
            print(f"Error: Price is missing or invalid for https://jlcpcb.com/partdetail/C{lcsc} ({price_json})")
    except (json.JSONDecodeError, ValueError, KeyError, TypeError):
        price_str = f""
        print(f"Error: Price cannot be parsed https://jlcpcb.com/partdetail/C{lcsc}")

    if price > 3.0 or footprint_name == "0201" or lcsc == 882967:
        df.drop(index=index, inplace=True)
    else:
        component_class = get_basic_or_prefered_type(df, index)
        stock = df.loc[index, "stock"]
        keywords = ""
        value = None

        datasheet = df.loc[index, "datasheet"]

        try:
            extra_json = json.loads(df.loc[index, "extra"])
            attributes = extra_json["attributes"]
            attributes = {key: value for key, value in attributes.items() if value != "-"}
        except:
            attributes = {}

        component_properties = {
            "price": price_str,
            "stock": stock,
            "datasheet": datasheet,
            "description": description,
            "process": assembly_process,
            "minimum qty": min_order_qty,
            "attrition qty": attrition_qty,
            "class": component_class,
            "category": category,
            "manufacturer": manufacturer,
            "part": manufacturerPartID,
        }

        component_properties = {**component_properties, **attributes}

        if df.loc[index, "category"] == "Resistors" and lcsc != 2909989:
            value = extract_resistance_value(description, lcsc)
            if "x4" in footprint_name:
                units = 4
            lib_name = "Resistors"

        elif df.loc[index, "category"] == "Capacitors":
            value = extract_capacitor_value(description, lcsc)
            lib_name = "Capacitors"
            if lcsc == 360353:
                footprint_name = "Plugin,P=5mm"
            if attributes == {}:
                # {'Voltage Rated': '50V', 'Tolerance': '±5%', 'Capacitance': '15pF', 'Temperature Coefficient': 'NP0'}
                capacitor_voltage = extract_capacitor_voltage(description, lcsc)
                if capacitor_voltage != None:
                    attributes = {"Voltage Rated": capacitor_voltage}

        elif df.loc[index, "category"] == "Diodes" or ("TVS" in subcategory) or ("ESD" in subcategory):
            value = extract_diode_type(description, joints, lcsc)
            secondary_mode = value
            lib_name = "Diodes"
            if value == None:
                if update_component_inplace(lcsc, "Diode-Packages", component_properties) == True:
                    df.drop(index=index, inplace=True)

        elif subcategory == "Light Emitting Diodes (LED)":
            if lcsc == 2895565 or lcsc == 2835341:
                if update_component_inplace(lcsc, "Diode-Packages", component_properties) == True:
                    df.drop(index=index, inplace=True)
            else:
                value, secondary_mode = extract_LED_value(description, lcsc)
                lib_name = "Diodes"

        elif (
            subcategory == "MOSFETs"
            or (subcategory == "Bipolar Transistors - BJT")
            or (subcategory == "Bipolar (BJT)")
            or (df.loc[index, "category"] == "Triode/MOS Tube/Transistor")
            or (df.loc[index, "category"] == "Transistors")
            or (df.loc[index, "category"] == "Transistors/Thyristors")
        ):
            if footprint_name == "SOT-23-3L" or footprint_name == "SOT-23-3":
                footprint_name = "SOT-23"
            elif footprint_name == "SOT-89-3":
                footprint_name = "SOT-89"

            value = extract_transistor_type(description, joints, footprint_name, lcsc)
            secondary_mode = value
            lib_name = "Transistors"
            if value == None:
                if update_component_inplace(lcsc, "Transistor-Packages", component_properties) == True:
                    df.drop(index=index, inplace=True)

        elif (
            subcategory == "Inductors (SMD)" or (subcategory == "Ferrite Beads") or (subcategory == "Power Inductors")
        ):
            value, secondary_mode = extract_inductor_type_value(description, joints, lcsc)
            lib_name = "Inductors"

        elif subcategory == "Crystals" or subcategory == "Oscillators":
            if update_component_inplace(lcsc, "Crystals", component_properties) == True:
                df.drop(index=index, inplace=True)

        elif (
            subcategory == "NTC Thermistors"
            or (subcategory == "Varistors")
            or (subcategory == "Fuses")
            or (subcategory == "Resettable Fuses")
        ):
            secondary_mode, value = extract_variable_resistor_type_value(description, lcsc)
            lib_name = "Variable-Resistors"
            if lcsc == 210465:
                footprint_name = "Plugin,P=5mm"

        elif df.loc[index, "category"] == "Embedded Processors & Controllers" or (
            df.loc[index, "category"] == "Single Chip Microcomputer/Microcontroller"
        ):
            del component_properties["datasheet"]
            del component_properties["description"]
            if update_component_inplace(lcsc, "MCUs", component_properties) == True:
                df.drop(index=index, inplace=True)

        elif (
            df.loc[index, "category"] == "Connectors"
            or (df.loc[index, "category"] == "Key/Switch")
            or (df.loc[index, "category"] == "Switches")
            or (lcsc == 2909989)
        ):
            if update_component_inplace(lcsc, "Connectors_Buttons", component_properties) == True:
                df.drop(index=index, inplace=True)

        elif (
            df.loc[index, "category"] == "Power Management"
            or (df.loc[index, "category"] == "Power Management ICs")
            or (lcsc == 394180)
        ):
            if update_component_inplace(lcsc, "Power", component_properties) == True:
                df.drop(index=index, inplace=True)

        elif (
            df.loc[index, "category"] == "Amplifiers"
            or (df.loc[index, "category"] == "Operational Amplifier/Comparator")
            or subcategory == "Analog Switches / Multiplexers"
            or subcategory == "Digital Potentiometers"
        ):
            if update_component_inplace(lcsc, "Analog", component_properties) == True:
                df.drop(index=index, inplace=True)

        elif df.loc[index, "category"] == "Memory":
            if update_component_inplace(lcsc, "Memory", component_properties) == True:
                df.drop(index=index, inplace=True)

        elif (
            df.loc[index, "category"] == "Communication Interface Chip"
            or (df.loc[index, "category"] == "Communication Interface Chip/UART/485/232")
            or (df.loc[index, "category"] == "Interface ICs")
            or (df.loc[index, "category"] == "Signal Isolation Devices")
        ):
            if update_component_inplace(lcsc, "Interface", component_properties) == True:
                df.drop(index=index, inplace=True)

        elif df.loc[index, "category"] == "Nixie Tube Driver/LED Driver" or (subcategory == "LCD Drivers"):
            if update_component_inplace(lcsc, "Display-Drivers", component_properties) == True:
                df.drop(index=index, inplace=True)

        elif (
            subcategory == "Current Transformers"
            or (subcategory == "Common Mode Filters")
            or (subcategory == "Color Ring Inductors / Through Hole Inductors")
        ):
            if update_component_inplace(lcsc, "Transformers", component_properties) == True:
                df.drop(index=index, inplace=True)

        elif (
            df.loc[index, "category"] == "Optocoupler"
            or (subcategory == "Optocouplers")
            or (subcategory == "Optocouplers - Phototransistor Output")
            or (subcategory == "Reflective Optical Interrupters")
        ):
            if update_component_inplace(lcsc, "Optocouplers", component_properties) == True:
                df.drop(index=index, inplace=True)

        elif (
            df.loc[index, "category"] == "Logic ICs"
            or (subcategory == "Real-time Clocks (RTC)")
            or (subcategory == "Timers / Clock Oscillators")
            or (subcategory == "Real-Time Clocks(RTC)")
            or (subcategory == "Clock Buffers/Drivers/Distributions")
            or (subcategory == "Hall Sensor")
        ):
            # print(f"{lcsc},")
            if update_component_inplace(lcsc, "ICs", component_properties) == True:
                df.drop(index=index, inplace=True)

        if value != None:
            df.drop(index=index, inplace=True)
            symbol = generate_kicad_symbol(
                lib_name,
                secondary_mode,
                lcsc,
                datasheet,
                description,
                footprint_name,
                value,
                keywords,
                price_str,
                assembly_process,
                min_order_qty,
                attrition_qty,
                component_class,
                stock,
                category,
                manufacturer,
                manufacturerPartID,
                attributes,
                units,
                footprints_lookup,
                names_lookup,
            )
            symbols[lib_name].append(symbol)

df.to_csv("leftover.csv", index=False)

generate_kicad_symbol_libs(symbols)

update_library_stock_inplace("Analog")
update_library_stock_inplace("Connectors_Buttons")
update_library_stock_inplace("Crystals")
update_library_stock_inplace("Diode-Packages")
update_library_stock_inplace("Display-Drivers")
update_library_stock_inplace("ICs")
update_library_stock_inplace("Interface")
update_library_stock_inplace("Memory")
update_library_stock_inplace("MCUs")
update_library_stock_inplace("Optocouplers")
update_library_stock_inplace("Power")
update_library_stock_inplace("Transformers")
update_library_stock_inplace("Transistor-Packages")

# check_footprints()
# check_models()

files_and_dirs = ['3dmodels', 'footprints', 'resources', 'symbols', 'metadata.json']
current_date = datetime.now(timezone.utc).strftime('%Y.%m.%d')

update_version('metadata.json', current_date)
create_zip_archive(f'JLCPCB-KiCad-Library-{current_date}.zip', files_and_dirs)

