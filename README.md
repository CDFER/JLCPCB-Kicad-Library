# JLCPCB-Kicad-Library
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A set of symbol Libararies and a set of footprints and 3d models of the basic components from JLCPCB smt assembly

Made using JLC2KiCadLib with manual touch ups.

## Features
- Supports JLCPCB Tools Plugin
- Contains every basic resistor and capacitor value
- Contains 3d models for 95%+ of the footprints
- Datasheet Links


## Basic Usage
Download this library and add it to your project like this

```
My_Kicad_Project
├── JLCPCB-Kicad-Library
│   ├── footprint
│   │   ├── packages3d
|   │   │   ├── CAP-SMD_L3.2-W1.6-RD-C7171.wrl
│   │   |   └── CRYSTAL-SMD_4P-L3.2-W2.5-BL.wrl
│   │   ├── CAP-SMD_L3.2-W1.6-RD-C7171.kicad_mod
│   │   └── CRYSTAL-SMD_4P-L3.2-W2.5-BL.kicad_mod
│   ├── jlcpcb-analog.kicad_sym
│   └── jlcpcb-basic-capacitor.kicad_sym
└── My_Kicad_Project.kicad_pro
```

Add the library in Kicad -> Prefrences -> Manage Symbol Libraries -> Project Specific Libraries -> Add exsisting Library to table -> Select all .kicad_sym files

Add the library in Kicad -> Prefrences -> Manage Footprint Libraries -> Project Specific Libraries -> Add exsisting Library to table -> Select footprint folder

## Git Submodule Use
Open Git Bash in the Kicad Project folder

```
$ git submodule add https://github.com/CDFER/JLCPCB-Kicad-Library.git
$ git submodule update --remote
```


## Notes

* Even though I have tested this libary, be careful and always check the output footprint and symbol.
* If you feel that an important feature is missing, please open an issue to discuss it, then you can fork this project with a new branch before submitting a PR. 

## License

This library is released under the MIT license

© 2023 Chris Dirks 
