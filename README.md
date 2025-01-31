# JLCPCB-KiCad-Library

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

A full KiCad library containing matched schematic symbols and PCB footprints, complete with 3D STEP models. All components are from JLCPCB's basic and preferred parts list, ensuring no extra setup costs.  I’m not affiliated or sponsored by jlcpcb, just another customer.

| KiCad 3d View | Fusion 360 |
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
* Minimum order quantity and attrition quantity provided for every component
* Utilizes .step files for seamless SolidWorks and Fusion 360 integration
* 99% of components include 3D models
* Datasheet links
* Supports JLCPCB Tools Plugin
* Built for KiCad 8+ (Currently seems to be stable with KiCad 9.0.0-RC2 too :)
* Allows you to export price to BOM

## Install using the package manager (new in V3.0)

Add my custom repository to the Plugin and Content Manager, the URL is:
```
https://raw.githubusercontent.com/CDFER/cd_fer-kicad-repository/main/repository.json
```

![Add My Custom Kicad Package Repo](images/Add_Custom_Repo.avif)

![Select My Custom Kicad Package Repo and press install](images/Select_Custom_Repo.avif)

After adding the repository link, press Save. Then, select CD_FER's KiCad repository from the dropdown menu and click on the JLCPCB KiCad Library. Finally, click the Install button and apply the pending changes.

## Notes

* Even though I have tested this library a number of times on pcb orders now, be careful and always check the output footprint and symbol.
* If you notice that anything is wrong or that an important feature is missing, please open an issue or pull request so it can be fixed.

## License

This library is released under the MIT license

© 2024 Chris Dirks
