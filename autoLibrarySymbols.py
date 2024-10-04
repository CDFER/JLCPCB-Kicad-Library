# librarySymbols.py

def generate_header(name):
    symbol = f'\t(symbol "{name}"'
    symbol += "\n\t\t(pin_numbers hide)"
    symbol += "\n\t\t(pin_names\n\t\t\t(offset 0)\n\t\t)"
    symbol += "\n\t\t(exclude_from_sim no)"
    symbol += "\n\t\t(in_bom yes)"
    symbol += "\n\t\t(on_board yes)"
    return symbol


def generate_property(key, value, at, size=1.27, hide="yes", autoplace=True):
    if autoplace == False:
        autoplace_str = "(do_not_autoplace)"
    else:
        autoplace_str = ""
    return f'\n\t\t(property "{key}" "{value}"\n\t\t\t(at {at}){autoplace_str}\n\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size {size} {size})\n\t\t\t\t)\n\t\t\t\t(hide {hide})\n\t\t\t)\n\t\t)'


def generate_rectangle(
    start,
    end,
    name,
    index,
    stroke={"width": 0.254, "type": "default"},
    fill={"type": "none"},
):
    return f'\n\t\t(symbol "{name}_{index}_1"\n\t\t\t(rectangle\n\t\t\t\t(start {start})\n\t\t\t\t(end {end})\n\t\t\t\t(stroke\n\t\t\t\t\t(width {stroke["width"]})\n\t\t\t\t\t(type {stroke["type"]})\n\t\t\t\t)\n\t\t\t\t(fill\n\t\t\t\t\t(type {fill["type"]})\n\t\t\t\t)\n\t\t\t)\n\t\t)'


def generate_polyline(
    points,
    name,
    index,
    stroke={"width": 0.254, "type": "default"},
    fill={"type": "none"},
):
    polyline_str = f'\n\t\t(symbol "{name}_{index}_1"\n\t\t\t(polyline\n\t\t\t\t(pts\n'
    for point in points:
        polyline_str += f"\t\t\t\t\t(xy {point})\n"
    polyline_str += f'\t\t\t\t)\n\t\t\t\t(stroke\n\t\t\t\t\t(width {stroke["width"]})\n\t\t\t\t\t(type {stroke["type"]})\n\t\t\t\t)\n\t\t\t\t(fill\n\t\t\t\t\t(type {fill["type"]})\n\t\t\t\t)\n\t\t\t)\n\t\t)'
    return polyline_str


def generate_pin_pair(pin_type, name, index, pin_length="1.27", pinA=1, pinB=2):
    symbol = f'\n\t\t(symbol "{name}_{index}_1"\n\t\t\t(pin {pin_type}\n\t\t\t\t(at 0 3.81 270)\n\t\t\t\t(length {pin_length})\n\t\t\t\t(name "~"\n\t\t\t\t\t(effects\n\t\t\t\t\t\t(font\n\t\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t\t)\n\t\t\t\t\t)\n\t\t\t\t)\n\t\t\t\t(number "{pinA}"\n\t\t\t\t\t(effects\n\t\t\t\t\t\t(font\n\t\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t\t)\n\t\t\t\t\t)\n\t\t\t\t)\n\t\t\t)'
    symbol += f'\n\t\t\t(pin {pin_type}\n\t\t\t\t(at 0 -3.81 90)\n\t\t\t\t(length {pin_length})\n\t\t\t\t(name "~"\n\t\t\t\t\t(effects\n\t\t\t\t\t\t(font\n\t\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t\t)\n\t\t\t\t\t)\n\t\t\t\t)\n\t\t\t\t(number "{pinB}"\n\t\t\t\t\t(effects\n\t\t\t\t\t\t(font\n\t\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t\t)\n\t\t\t\t\t)\n\t\t\t\t)\n\t\t\t)'
    symbol += "\n\t\t)"
    return symbol


def generate_kicad_symbol(
    mode,
    secondary_mode,
    lcsc,
    datasheet,
    description,
    footprint,
    value,
    keywords,
    price,
    component_class,
    stock,
    category,
    manufacturer,
    manufacturerPartID,
    attributes,
    units,
    footprints_lookup,
    names_lookup
):
    if mode == "Resistors":
        ref_designator = "R"
        ref_position = "2.032 0 0"
        value_position = "0 0 90"
        value_autoplace = False
        name = f"{footprint},{value}"

    elif mode == "Capacitors":
        ref_designator = "C"
        ref_position = "2.032 0 0"
        value_position = "3.556 -1.524 0"
        value_autoplace = True
        name = f"{footprint},{value}"

    elif mode == "Diodes":
        ref_designator = "D"
        ref_position = "2.032 0.834 0"
        value_position = "2.032 -1.2122 0"
        value_autoplace = True
        if secondary_mode == "LED" or secondary_mode == "LED-Bi-Colour":
            name = f"{secondary_mode},{footprint},{value}"
        else:
            name = f"{value},{manufacturerPartID}"
            value = manufacturerPartID

    elif mode == "Inductors":
        if secondary_mode == "Inductor":
            ref_designator = "L"
            name = f"{value}"
        elif secondary_mode == "Ferrite":
            ref_designator = "FB"
            name = f"Ferrite,{footprint}"
        ref_position = "2.032 0 0"
        value_position = "3.556 -1.524 0"
        value_autoplace = True

    elif mode == "Transistors":
        ref_designator = "Q"
        ref_position = "4.8514 0.834 0"
        value_position = "4.8514 -1.2122 0"
        value_autoplace = True
        # Remove brackets from manufacturerPartID
        cleaned_manufacturerPartID = (
            manufacturerPartID.replace("(", "").replace(")", "").replace("RANGE:", " ")
        )
        name = f"{value},{cleaned_manufacturerPartID}"
        value = cleaned_manufacturerPartID

    else:
        ref_designator = "NA"
        ref_position = "0 0 0"
        value_position = "0 0 0"
        value_autoplace = True
        name = f"{footprint},{value}"
    lcsc = f"C{lcsc}"

    if footprint == "SMA(DO-214AC)":
        footprint = "SMA"
    if footprint == "SMB(DO-214AA)":
        footprint = "SMB"
    if footprint == "SOT-23-3":
        footprint = "SOT-23"

    # if f"{ref_designator}_{footprint}" not in footprints_lookup:
    #     missing_footprint = f"{ref_designator}_{footprint}"
    #     if missing_footprint in missing_footprints:
    #         missing_footprints[missing_footprint] += 1
    #     else:
    #         missing_footprints[missing_footprint] = 1
    if name in names_lookup:
        if name + ",(2)" not in names_lookup:
            name = name + ",(2)"
        elif name + ",(3)" not in names_lookup:
            name = name + ",(3)"
        elif name + ",(4)" not in names_lookup:
            name = name + ",(4)"
        elif name + ",(5)" not in names_lookup:
            name = name + ",(5)"
        elif name + ",(6)" not in names_lookup:
            name = name + ",(6)"
        else:
            print("more than 5 symbols with the same name...")

    names_lookup.append(name)
    

    footprint = f"JLCPCB-Kicad-Footprints:{ref_designator}_{footprint}"

    symbol = generate_header(name)

    symbol += generate_property("Reference", ref_designator, ref_position, hide="no")
    symbol += generate_property(
        "Value", value, value_position, size=0.8, hide="no", autoplace=value_autoplace
    )
    symbol += generate_property("Footprint", footprint, "-1.778 0 90")
    symbol += generate_property("Datasheet", datasheet, "0 0 0")
    symbol += generate_property("Description", description, "0 0 0")
    symbol += generate_property("LCSC", lcsc, "0 0 0")
    symbol += generate_property("Price", price, "0 0 0")
    symbol += generate_property("Class", component_class, "0 0 0")
    symbol += generate_property("Stock", stock, "0 0 0")
    symbol += generate_property("Category", category, "0 0 0")
    symbol += generate_property("Manufacturer", manufacturer, "0 0 0")
    symbol += generate_property("Manufacturer Part ID", manufacturerPartID, "0 0 0")

    if type(attributes) == dict:
        for key, value in attributes.items():
            symbol += generate_property(f"{key}", f"{value}", "0 0 0")

    symbol += generate_property("ki_keywords", keywords, at="0 0 0")
    symbol += generate_property("ki_fp_filters", f"{ref_designator}_*", "0 0 0")

    if mode == "Resistors":
        symbol += generate_rectangle("-1.016 2.54", "1.016 -2.54", name=name, index=0)
        for i in range(1, units + 1):
            symbol += generate_pin_pair(
                "passive line", name, i, "1.27", i, (units * 2) - (i - 1)
            )

    elif mode == "Capacitors":
        symbol += generate_polyline(["-1.27 0.635", "1.27 0.635"], name=name, index=0)
        symbol += generate_polyline(["-1.27 -0.635", "1.27 -0.635"], name=name, index=0)
        polarized_footprints = [
            "C_Plugin,D5xL11mm",
            "C_Plugin,D10xL12.5mm",
            "C_CASE-B-3528-21(mm)",
            "C_CASE-A-3216-18(mm)",
        ]
        if any(s in footprint for s in polarized_footprints):
            symbol += generate_polyline(
                ["-1.27 1.27", "-0.635 1.27"],
                name=name,
                index=0,
                stroke={"width": 0.127, "type": "default"},
            )
            symbol += generate_polyline(
                ["-0.9525 1.5875", "-0.9525 0.9525"],
                name=name,
                index=0,
                stroke={"width": 0.127, "type": "default"},
            )
        for i in range(1, units + 1):
            symbol += generate_pin_pair(
                "passive line", name, i, "3.175", i, (units * 2) - (i - 1)
            )

    elif mode == "Diodes":
        if secondary_mode == "Bridge-Rectifier":
            symbol += generate_rectangle("-2.54 2.54", "2.54 -2.54", name=name, index=0)
        elif secondary_mode == "TVS-Bi":
            symbol += generate_polyline(
                ["-1.27 2.54", "0 0", "1.27 2.54", "-1.27 2.54"], name=name, index=0
            )
            symbol += generate_polyline(
                ["1.27 -2.54", "0 0", "-1.27 -2.54", "1.27 -2.54"], name=name, index=0
            )
            symbol += generate_polyline(
                ["-1.905 -0.635", "-1.27 0", "1.27 0", "1.905 0.635"],
                name=name,
                index=0,
            )
            for i in range(1, units + 1):
                symbol += generate_pin_pair(
                    "passive line", name, i, "3.81", (units * 2) - (i - 1), i
                )
        elif secondary_mode == "LED-Bi-Colour":
            symbol += generate_polyline(
                ["-3.175 -1.27", "-0.635 -1.27"], name=name, index=0
            )
            symbol += generate_polyline(
                ["3.175 1.27", "0.635 1.27"], name=name, index=0
            )
            symbol += generate_polyline(
                ["-3.175 1.27", "-1.905 -1.27", "-0.635 1.27", "-3.175 1.27"],
                name=name,
                index=0,
            )
            symbol += generate_polyline(
                ["-1.905 -1.27", "-1.905 -2.54", "1.905 -2.54", "1.905 -1.27"],
                name=name,
                index=0,
            )
            symbol += generate_polyline(
                ["-1.905 1.27", "-1.905 2.54", "1.905 2.54", "1.905 1.27"],
                name=name,
                index=0,
            )
            symbol += generate_polyline(
                ["3.175 -1.27", "1.905 1.27", "0.635 -1.27", "3.175 -1.27"],
                name=name,
                index=0,
            )
            symbol += generate_polyline(
                [
                    "-3.81 -1.27",
                    "-5.334 0.254",
                    "-5.334 -0.254",
                    "-5.334 0.254",
                    "-4.826 0.254",
                ],
                name=name,
                index=0,
                stroke={"width": 0.127, "type": "default"},
            )
            symbol += generate_polyline(
                [
                    "-3.81 0",
                    "-5.334 1.524",
                    "-5.334 1.016",
                    "-5.334 1.524",
                    "-4.826 1.524",
                ],
                name=name,
                index=0,
                stroke={"width": 0.127, "type": "default"},
            )
            symbol += generate_polyline(
                [
                    "3.81 0",
                    "5.334 -1.524",
                    "5.334 -1.016",
                    "5.334 -1.524",
                    "4.826 -1.524",
                ],
                name=name,
                index=0,
                stroke={"width": 0.127, "type": "default"},
            )
            symbol += generate_polyline(
                [
                    "3.81 1.27",
                    "5.334 -0.254",
                    "5.334 0.254",
                    "5.334 -0.254",
                    "4.826 -0.254",
                ],
                name=name,
                index=0,
                stroke={"width": 0.127, "type": "default"},
            )
            symbol += generate_pin_pair("passive line", name, 1, "1.27", 1, 2)
        else:
            symbol += generate_polyline(
                ["-1.27 1.27", "0.00 -1.27", "1.27 1.27", "-1.27 1.27"],
                name=name,
                index=0,
            )
            if secondary_mode == "Schottky":
                symbol += generate_polyline(
                    [
                        "0.635 -1.905",
                        "1.27 -1.905",
                        "1.27 -1.27",
                        "-1.27 -1.27",
                        "-1.27 -0.635",
                        "-0.635 -0.635",
                    ],
                    name=name,
                    index=0,
                )
            elif secondary_mode == "Zener":
                symbol += generate_polyline(
                    ["-1.27 -1.27", "1.27 -1.27", "1.27 -0.762"], name=name, index=0
                )
            elif secondary_mode == "TVS-Uni":
                symbol += generate_polyline(
                    ["-1.905 -1.905", "-1.27 -1.27", "1.27 -1.27", "1.905 -0.635"],
                    name=name,
                    index=0,
                )
            elif secondary_mode == "LED":
                symbol += generate_polyline(
                    ["-1.27 -1.27", "1.27 -1.27"], name=name, index=0
                )
                symbol += generate_polyline(
                    [
                        "-1.905 -1.27",
                        "-3.429 0.254",
                        "-3.429 -0.254",
                        "-3.429 0.254",
                        "-2.921 0.254",
                    ],
                    name=name,
                    index=0,
                    stroke={"width": 0.127, "type": "default"},
                )
                symbol += generate_polyline(
                    [
                        "-1.905 0",
                        "-3.429 1.524",
                        "-3.429 1.016",
                        "-3.429 1.524",
                        "-2.921 1.524",
                    ],
                    name=name,
                    index=0,
                    stroke={"width": 0.127, "type": "default"},
                )
            else:
                symbol += generate_polyline(
                    ["-1.27 -1.27", "1.27 -1.27"], name=name, index=0
                )

            for i in range(1, units + 1):
                symbol += generate_pin_pair(
                    "passive line", name, i, "3.81", (units * 2) - (i - 1), i
                )

    elif mode == "Transistors":
        if secondary_mode == "NPN":
            npn = f"""		(symbol "{name}_0_1"
            (polyline
                (pts
                    (xy -2.54 0) (xy 0.635 0)
                )
                (stroke
                    (width 0.1524)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (polyline
                (pts
                    (xy 0.635 0.635) (xy 2.54 2.54)
                )
                (stroke
                    (width 0)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (polyline
                (pts
                    (xy 2.794 -1.27) (xy 2.794 -1.27)
                )
                (stroke
                    (width 0.1524)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (polyline
                (pts
                    (xy 2.794 -1.27) (xy 2.794 -1.27)
                )
                (stroke
                    (width 0.1524)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (polyline
                (pts
                    (xy 0.635 -0.635) (xy 2.54 -2.54) (xy 2.54 -2.54)
                )
                (stroke
                    (width 0)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (polyline
                (pts
                    (xy 0.635 1.905) (xy 0.635 -1.905) (xy 0.635 -1.905)
                )
                (stroke
                    (width 0.508)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (polyline
                (pts
                    (xy 1.27 -1.778) (xy 1.778 -1.27) (xy 2.286 -2.286) (xy 1.27 -1.778) (xy 1.27 -1.778)
                )
                (stroke
                    (width 0)
                    (type default)
                )
                (fill
                    (type outline)
                )
            )
            (circle
                (center 1.27 0)
                (radius 2.8194)
                (stroke
                    (width 0.254)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
        )
        (symbol "{name}_1_1"
            (pin open_collector line
                (at 2.54 5.08 270)
                (length 2.54)
                (name "C"
                    (effects
                        (font
                            (size 1.27 1.27)
                        )
                    )
                )
                (number "1"
                    (effects
                        (font
                            (size 1.27 1.27)
                        )
                    )
                )
            )
            (pin input line
                (at -5.08 0 0)
                (length 2.54)
                (name "B"
                    (effects
                        (font
                            (size 1.27 1.27)
                        )
                    )
                )
                (number "2"
                    (effects
                        (font
                            (size 1.27 1.27)
                        )
                    )
                )
            )
            (pin open_emitter line
                (at 2.54 -5.08 90)
                (length 2.54)
                (name "E"
                    (effects
                        (font
                            (size 1.27 1.27)
                        )
                    )
                )
                (number "3"
                    (effects
                        (font
                            (size 1.27 1.27)
                        )
                    )
                )
            )
        )"""
            symbol += npn
        elif secondary_mode == "PNP":
            pnp = f"""		(symbol "{name}_0_1"
            (polyline
                (pts
                    (xy -2.54 0) (xy 0.635 0)
                )
                (stroke
                    (width 0.1524)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (polyline
                (pts
                    (xy 0.635 0.635) (xy 2.54 2.54)
                )
                (stroke
                    (width 0)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (polyline
                (pts
                    (xy 0.635 -0.635) (xy 2.54 -2.54) (xy 2.54 -2.54)
                )
                (stroke
                    (width 0)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (polyline
                (pts
                    (xy 0.635 1.905) (xy 0.635 -1.905) (xy 0.635 -1.905)
                )
                (stroke
                    (width 0.508)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (polyline
                (pts
                    (xy 2.286 -1.778) (xy 1.778 -2.286) (xy 1.27 -1.27) (xy 2.286 -1.778) (xy 2.286 -1.778)
                )
                (stroke
                    (width 0)
                    (type default)
                )
                (fill
                    (type outline)
                )
            )
            (circle
                (center 1.27 0)
                (radius 2.8194)
                (stroke
                    (width 0.254)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
        )
        (symbol "{name}_1_1"
            (pin open_collector line
                (at 2.54 5.08 270)
                (length 2.54)
                (name "C"
                    (effects
                        (font
                            (size 1.27 1.27)
                        )
                    )
                )
                (number "1"
                    (effects
                        (font
                            (size 1.27 1.27)
                        )
                    )
                )
            )
            (pin input line
                (at -5.08 0 0)
                (length 2.54)
                (name "B"
                    (effects
                        (font
                            (size 1.27 1.27)
                        )
                    )
                )
                (number "2"
                    (effects
                        (font
                            (size 1.27 1.27)
                        )
                    )
                )
            )
            (pin open_emitter line
                (at 2.54 -5.08 90)
                (length 2.54)
                (name "E"
                    (effects
                        (font
                            (size 1.27 1.27)
                        )
                    )
                )
                (number "3"
                    (effects
                        (font
                            (size 1.27 1.27)
                        )
                    )
                )
            )
        )"""
            symbol += pnp
        elif secondary_mode == "NMOS":
            nmos = f"""		(symbol "{name}_0_1"
            (polyline
                (pts
                    (xy 0.254 0) (xy -2.54 0)
                )
                (stroke
                    (width 0)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (polyline
                (pts
                    (xy 0.254 1.905) (xy 0.254 -1.905)
                )
                (stroke
                    (width 0.254)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (polyline
                (pts
                    (xy 0.762 -1.27) (xy 0.762 -2.286)
                )
                (stroke
                    (width 0.254)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (polyline
                (pts
                    (xy 0.762 0.508) (xy 0.762 -0.508)
                )
                (stroke
                    (width 0.254)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (polyline
                (pts
                    (xy 0.762 2.286) (xy 0.762 1.27)
                )
                (stroke
                    (width 0.254)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (polyline
                (pts
                    (xy 2.54 2.54) (xy 2.54 1.778)
                )
                (stroke
                    (width 0)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (polyline
                (pts
                    (xy 2.54 -2.54) (xy 2.54 0) (xy 0.762 0)
                )
                (stroke
                    (width 0)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (polyline
                (pts
                    (xy 0.762 -1.778) (xy 3.302 -1.778) (xy 3.302 1.778) (xy 0.762 1.778)
                )
                (stroke
                    (width 0)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (polyline
                (pts
                    (xy 1.016 0) (xy 2.032 0.381) (xy 2.032 -0.381) (xy 1.016 0)
                )
                (stroke
                    (width 0)
                    (type default)
                )
                (fill
                    (type outline)
                )
            )
            (polyline
                (pts
                    (xy 2.794 0.508) (xy 2.921 0.381) (xy 3.683 0.381) (xy 3.81 0.254)
                )
                (stroke
                    (width 0)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (polyline
                (pts
                    (xy 3.302 0.381) (xy 2.921 -0.254) (xy 3.683 -0.254) (xy 3.302 0.381)
                )
                (stroke
                    (width 0)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (circle
                (center 1.651 0)
                (radius 2.794)
                (stroke
                    (width 0.254)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (circle
                (center 2.54 -1.778)
                (radius 0.254)
                (stroke
                    (width 0)
                    (type default)
                )
                (fill
                    (type outline)
                )
            )
            (circle
                (center 2.54 1.778)
                (radius 0.254)
                (stroke
                    (width 0)
                    (type default)
                )
                (fill
                    (type outline)
                )
            )
        )
        (symbol "{name}_1_1"
            (pin passive line
                (at 2.54 5.08 270)
                (length 2.54)
                (name "D"
                    (effects
                        (font
                            (size 1.27 1.27)
                        )
                    )
                )
                (number "1"
                    (effects
                        (font
                            (size 1.27 1.27)
                        )
                    )
                )
            )
            (pin input line
                (at -5.08 0 0)
                (length 2.54)
                (name "G"
                    (effects
                        (font
                            (size 1.27 1.27)
                        )
                    )
                )
                (number "2"
                    (effects
                        (font
                            (size 1.27 1.27)
                        )
                    )
                )
            )
            (pin passive line
                (at 2.54 -5.08 90)
                (length 2.54)
                (name "S"
                    (effects
                        (font
                            (size 1.27 1.27)
                        )
                    )
                )
                (number "3"
                    (effects
                        (font
                            (size 1.27 1.27)
                        )
                    )
                )
            )
        )"""
            symbol += nmos
        elif secondary_mode == "PMOS":
            pmos = f"""		(symbol "{name}_0_1"
            (polyline
                (pts
                    (xy 0.254 0) (xy -2.54 0)
                )
                (stroke
                    (width 0)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (polyline
                (pts
                    (xy 0.254 1.905) (xy 0.254 -1.905)
                )
                (stroke
                    (width 0.254)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (polyline
                (pts
                    (xy 0.762 -1.27) (xy 0.762 -2.286)
                )
                (stroke
                    (width 0.254)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (polyline
                (pts
                    (xy 0.762 0.508) (xy 0.762 -0.508)
                )
                (stroke
                    (width 0.254)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (polyline
                (pts
                    (xy 0.762 2.286) (xy 0.762 1.27)
                )
                (stroke
                    (width 0.254)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (polyline
                (pts
                    (xy 2.54 2.54) (xy 2.54 1.778)
                )
                (stroke
                    (width 0)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (polyline
                (pts
                    (xy 2.54 -2.54) (xy 2.54 0) (xy 0.762 0)
                )
                (stroke
                    (width 0)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (polyline
                (pts
                    (xy 0.762 1.778) (xy 3.302 1.778) (xy 3.302 -1.778) (xy 0.762 -1.778)
                )
                (stroke
                    (width 0)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (polyline
                (pts
                    (xy 2.286 0) (xy 1.27 0.381) (xy 1.27 -0.381) (xy 2.286 0)
                )
                (stroke
                    (width 0)
                    (type default)
                )
                (fill
                    (type outline)
                )
            )
            (polyline
                (pts
                    (xy 2.794 -0.508) (xy 2.921 -0.381) (xy 3.683 -0.381) (xy 3.81 -0.254)
                )
                (stroke
                    (width 0)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (polyline
                (pts
                    (xy 3.302 -0.381) (xy 2.921 0.254) (xy 3.683 0.254) (xy 3.302 -0.381)
                )
                (stroke
                    (width 0)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (circle
                (center 1.651 0)
                (radius 2.794)
                (stroke
                    (width 0.254)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            (circle
                (center 2.54 -1.778)
                (radius 0.254)
                (stroke
                    (width 0)
                    (type default)
                )
                (fill
                    (type outline)
                )
            )
            (circle
                (center 2.54 1.778)
                (radius 0.254)
                (stroke
                    (width 0)
                    (type default)
                )
                (fill
                    (type outline)
                )
            )
        )
        (symbol "{name}_1_1"
            (pin passive line
                (at 2.54 5.08 270)
                (length 2.54)
                (name "D"
                    (effects
                        (font
                            (size 1.27 1.27)
                        )
                    )
                )
                (number "1"
                    (effects
                        (font
                            (size 1.27 1.27)
                        )
                    )
                )
            )
            (pin input line
                (at -5.08 0 0)
                (length 2.54)
                (name "G"
                    (effects
                        (font
                            (size 1.27 1.27)
                        )
                    )
                )
                (number "2"
                    (effects
                        (font
                            (size 1.27 1.27)
                        )
                    )
                )
            )
            (pin passive line
                (at 2.54 -5.08 90)
                (length 2.54)
                (name "S"
                    (effects
                        (font
                            (size 1.27 1.27)
                        )
                    )
                )
                (number "3"
                    (effects
                        (font
                            (size 1.27 1.27)
                        )
                    )
                )
            )
        )"""
            symbol += pmos
        else:
            symbol += generate_rectangle("-2.54 2.54", "2.54 -2.54", name=name, index=0)
            
    elif mode == "Inductors":
        if secondary_mode == "Ferrite":
            ferrite = f"""		(symbol "{name}_0_1"
			(polyline
				(pts
					(xy 0 -1.27) (xy 0 -1.2192)
				)
				(stroke
					(width 0)
					(type default)
				)
				(fill
					(type none)
				)
			)
			(polyline
				(pts
					(xy 0 1.27) (xy 0 1.2954)
				)
				(stroke
					(width 0)
					(type default)
				)
				(fill
					(type none)
				)
			)
			(polyline
				(pts
					(xy -2.7686 0.4064) (xy -1.7018 2.2606) (xy 2.7686 -0.3048) (xy 1.6764 -2.159) (xy -2.7686 0.4064)
				)
				(stroke
					(width 0)
					(type default)
				)
				(fill
					(type none)
				)
			)
		)
		(symbol "{name}_1_1"
			(pin passive line
				(at 0 3.81 270)
				(length 2.54)
				(name "~"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
				(number "1"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
			(pin passive line
				(at 0 -3.81 90)
				(length 2.54)
				(name "~"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
				(number "2"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
		)"""
            symbol+=ferrite
            
        elif secondary_mode == "Inductor":
            inductor = f"""		(symbol "{name}_0_1"
			(arc
				(start 0 -2.54)
				(mid 0.6323 -1.905)
				(end 0 -1.27)
				(stroke
					(width 0)
					(type default)
				)
				(fill
					(type none)
				)
			)
			(arc
				(start 0 -1.27)
				(mid 0.6323 -0.635)
				(end 0 0)
				(stroke
					(width 0)
					(type default)
				)
				(fill
					(type none)
				)
			)
			(arc
				(start 0 0)
				(mid 0.6323 0.635)
				(end 0 1.27)
				(stroke
					(width 0)
					(type default)
				)
				(fill
					(type none)
				)
			)
			(arc
				(start 0 1.27)
				(mid 0.6323 1.905)
				(end 0 2.54)
				(stroke
					(width 0)
					(type default)
				)
				(fill
					(type none)
				)
			)
		)
		(symbol "{name}_1_1"
			(pin passive line
				(at 0 3.81 270)
				(length 1.27)
				(name "~"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
				(number "1"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
			(pin passive line
				(at 0 -3.81 90)
				(length 1.27)
				(name "~"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
				(number "2"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
		)"""
            symbol+=inductor

    symbol += "\n\t)"
    return symbol
