# JLCPCB-Kicad-Library

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A full KiCad library containing matched schematic symbols and PCB footprints, complete with 3D STEP models. All components are from JLCPCB's basic and preferred parts list, ensuring no extra setup costs.

| Kicad 3d View | Fusion 360 |
|:-------------------------:|:-------------------------:|
|![3D Component Sample](images/3D_Sample.avif)|![3D Component Sample in Fusion 360](images/3D_Sample_Fusion360.avif)|

## Screenshots

| | |
|:-------------------------:|:-------------------------:|
|<img width="400" alt="R0402x4 Symbol Selection" src="images/Choose_Symbol_R0402x4.avif">|<img width="400" alt="Boost Symbol Selection" src="images/Choose_Symbol_Boost.avif">|

![Schematic Buck](images/Schematic_Buck.avif)
![Choose BOM Fields](images/Choose_BOM.avif)
![Output BOM csv file](images/Output_BOM.avif)

## Features

* Daily updated stock and pricing information (uses Github Actions)
* Utilizes .step files for seamless SolidWorks and Fusion 360 integration
* 99% of components include 3D models
* Datasheet links
* Supports JLCPCB Tools Plugin
* Optimized for KiCad 8
* Allows you to export price to BOM

## Manual Setup

1. Download the library.
2. Place it within your KiCad project folder.

```
My_Kicad_Project_Folder
├── JLCPCB-Kicad-Library-Folder
└── My_Kicad_Project.kicad_pro
```

3. Add libraries in KiCad:

* Add the library in Kicad -> Preferences -> Manage Symbol Libraries -> Project Specific Libraries -> Add existing Library to table -> Select all .kicad_sym files in the JLCPCB-Kicad-Symbols folder
* Add the library in Kicad -> Preferences -> Manage Footprint Libraries -> Project Specific Libraries -> Add existing Library to table -> Select the JLCPCB-Kicad-Footprints folder

If you have any issues setting it up feel free to post an issue :)

## Git Submodule Setup (allows you to automatically update pricing and stock)

Open Git Bash in the Kicad Project folder (in the right click menu on windows if you have git installed)

```Bash
$ git submodule add https://github.com/CDFER/JLCPCB-Kicad-Library.git
```

and to update it all you need to run to update is:

```Bash
$ git submodule update --remote
```

## Notes

* Even though I have tested this library a number of times on pcb orders now, be careful and always check the output footprint and symbol.
* If you notice that anything is wrong or that an important feature is missing, please open an issue or pull request so it can be fixed.

## License

This library is released under the MIT license

© 2024 Chris Dirks
