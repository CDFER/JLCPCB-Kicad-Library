# handmadeLibrarySymbols.py
import os

stock_price_str = """		(property "Stock" "1"
			(at 0 0 0)
			(effects
				(font
					(size 1.27 1.27)
				)
				(hide yes)
			)
		)
		(property "Price" "1.00USD"
			(at 0 0 0)
			(effects
				(font
					(size 1.27 1.27)
				)
				(hide yes)
			)
		)\n"""

def update_component_inplace(lcsc, libraryName, price, stock, datasheet = None, description = None):
	filename = os.path.join("JLCPCB-Kicad-Symbols", f"JLCPCB-{libraryName}.kicad_sym")
	with open(filename, "r") as file:
		lines = file.readlines()

	lcsc_found = False
	price_found = False
	stock_found = False
	keywords_index = 0

	for i, line in enumerate(lines):
		if lcsc_found == False:
			if f'(property "LCSC" "C{lcsc}"' in line:
				lcsc_found = True
				line_offset = 1
				# print(f"Found {lcsc} on line {i} of {filename}")
				# Work Upwards to find datasheet
				if (datasheet != None) or (description != None):
					while ('(symbol' not in lines[i - line_offset]) and (line_offset < 30):
						if '(property "Datasheet"' in lines[i - line_offset] and (datasheet != None):
							lines[i - line_offset] = f'		(property "Datasheet" "{datasheet}"\n'
						elif '(property "Description"' in lines[i - line_offset] and (description != None):
							lines[i - line_offset] = f'		(property "Description" "{description}"\n'
						line_offset+=1

		else:
			if '(property "Price"' in line:
				lines[i] = f'		(property "Price" "{price}USD"\n'
				price_found = True
			elif '(property "ki_keywords"' in line:
				keywords_index = i
			elif '(property "Stock"' in line:
				lines[i] = f'		(property "Stock" "{stock}"\n'
				stock_found = True
			elif '(symbol' in line:
				lines.insert(keywords_index,stock_price_str)
				print(f"Error Missing Price or Stock property in file keywords index:{keywords_index}, lines {len(lines)}")
				break
			if price_found and stock_found:
				break

	if lcsc_found == False:
		print(
			f"Error: C{lcsc} not found in library {filename}, Found: LCSC={lcsc_found}, Price={price_found}, Stock={stock_found}"
		)
		return False
	else:
		with open(filename, "w") as file:
			file.writelines(lines)
			return True
