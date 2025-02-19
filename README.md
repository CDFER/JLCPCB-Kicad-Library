# JLCPCB-KiCad-Library

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

A full KiCad library containing matched schematic symbols and PCB footprints, complete with 3D STEP models. This Library is focused on components from JLCPCB's **basic and preferred** parts list, ensuring no extra setup costs.  I’m not affiliated or sponsored by jlcpcb, just another customer.

## Screenshots

| KiCad | Fusion 360 |
|:-------------------------:|:-------------------------:|
|![3D Component Sample](images/3D_Sample.avif)|![3D Component Sample in Fusion 360](images/3D_Sample_Fusion360.avif)|

| | |
|:-------------------------:|:-------------------------:|
|<img width="400" alt="Diode Symbol Selection" src="images/Choose_Symbol_SS54.avif">|<img width="400" alt="Buck Converter Symbol Selection" src="images/Choose_Symbol_Buck.avif">|

![Schematic Buck](images/Schematic_Buck.avif)

## Features

* Daily updated stock and pricing information (uses Github Actions)
* Minimum order quantity and attrition quantity provided for every component
* Utilizes .step files for seamless SolidWorks and Fusion 360 integration
* 99% of components include 3D models
* Datasheet links
* Supports Bouni's [JLCPCB Tools Plugin](https://github.com/Bouni/kicad-jlcpcb-tools)
* Built for KiCad 8+ (Currently seems to be stable with KiCad 9.0.0-RC2 too :)
* Allows you to export price to BOM

## Install using the package manager

Add my custom repository to the Plugin and Content Manager, the URL is:

```
https://raw.githubusercontent.com/CDFER/cd_fer-kicad-repository/main/repository.json
```

![Add My Custom Kicad Package Repo](images/Add_Custom_Repo.avif)

![Select My Custom Kicad Package Repo and press install](images/Select_Custom_Repo.avif)

After adding the repository link, press Save. Then, select CD_FER's KiCad repository from the dropdown menu and click on the JLCPCB KiCad Library. Finally, click the Install button and apply the pending changes.

### Install Guide Video

Thanks to Rob Frohne for putting the time in to make a video to guide you through how to install the library

[**▶️ Watch the Install Guide Video**](https://www.youtube.com/watch?v=Bf6XzcvVBs4)

### Updating the Library

KiCad currently doesn't support fully automatic updates but it does notify you and you then have to manually navigate the installed libraries, click to update it and apply pending changes (yeah it's a bit annoying).

![Package Update Warning](images/Update_Package_Warning.avif)

![Add My Custom Kicad Package Repo](images/Update_Package.avif)

## Notes

* Even though I have tested this library a number of times on pcb orders now, be careful and always check the output footprint and symbol.
* If you notice that anything is wrong or that an important feature is missing, please open an issue or pull request so it can be fixed.

### What is Attrition Quantity?

**Attrition Quantity** is the number of parts that get wasted when setting up the machine (like during adjustments or errors).  

When you order parts, you need to buy **either**:  

1. The **minimum amount** the supplier allows (**JLCPCB’s minimum order quantity**), *or*

2. **Enough for your product** (total parts needed) **+ extra** to cover wasted parts during setup.  

**Example**:  
If you’re making 5 circuit boards, and each needs 10 resistors, you’d need 50 resistors. But if you expect 2 parts to be wasted (attrition), order **52 resistors total** (or the JLCPCB minimum, if it’s higher).  

## License

This library is released under the MIT license

© 2024 Chris Dirks
