# handmadeLibrarySymbols.py
import os


def update_component_inplace(lcsc, libraryName, price, stock):
	filename = os.path.join("JLCPCB-Kicad-Symbols", f"JLCPCB-{libraryName}.kicad_sym")
	with open(filename, "r") as file:
		lines = file.readlines()

	lcsc_found = False
	price_found = False
	stock_found = False

	for i, line in enumerate(lines):
		if lcsc_found == False:
			if f'(property "LCSC" "C{lcsc}"' in line:
				lcsc_found = True
				# print(f"Found {lcsc} on line {i} of {filename}")

		else:
			if '(property "Price"' in line:
				lines[i] = f'		(property "Price" "{price}USD"\n'
				price_found = True
			elif '(property "Stock"' in line:
				lines[i] = f'		(property "Stock" "{stock}"\n'
				stock_found = True
			elif '(property "LCSC"' in line:
				# print("Error Missing Price or Stock property in file")
				break
			if price_found and stock_found:
				break

	if lcsc_found and price_found and stock_found:
		with open(filename, "w") as file:
			file.writelines(lines)
			return True
	else:
		print(
			f"Error: C{lcsc} not found in library {filename}, Found: LCSC={lcsc_found}, Price={price_found}, Stock={stock_found}"
		)

	return False
