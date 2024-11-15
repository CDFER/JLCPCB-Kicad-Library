# handmadeLibrarySymbols.py
import os
import pandas as pd
import re

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
		archived_symbol_path = os.path.join('Archived-Symbols-Footprints', 'JLCPCB-Kicad-Symbols')
		archived_symbols_lcsc = [os.path.splitext(filename)[0] 
					for filename in os.listdir(archived_symbol_path) 
					if filename.endswith('.kicad_sym')]
		if f'{lcsc}' in archived_symbols_lcsc:
			print(f"Error: C{lcsc} not found in library {filename} but it was found in the archive folder: {archived_symbol_path}")
		else:
			print(f"Error: C{lcsc} not found in library {filename}")
		return False
	else:
		with open(filename, "w") as file:
			file.writelines(lines)
			return True

symbol_header_lines = '''(kicad_symbol_lib
	(version 20231120)
	(generator "CDFER_Archive_Tool")
	(generator_version "0.0")
 '''

symbol_footer_lines = ''')
'''

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
	filename = os.path.join("JLCPCB-Kicad-Symbols", f"JLCPCB-{libraryName}.kicad_sym")
	with open(filename, "r") as file:
		lines = file.readlines()
	
	no_stock = False
	lcsc = 0
	symbol_start_line = 0
	
	for i, line in enumerate(lines):
		lines[i] = lines[i].replace("℃", "°C")
		if line.startswith('\t(') or line.startswith(')'):
			if no_stock == True:
				create_archived_symbol_file(symbol_start_line, i, lines, lcsc)
				lines[symbol_start_line:i] = [''] * (i - symbol_start_line) # Remove symbol from library by replacing lines with empty strings
				no_stock = False
			symbol_start_line=i
	
		elif '(property "LCSC" "C' in line:
			# print(f"LCSC Found on line {i} {line}")
			numbers = [int(num) for num in re.findall('\\d+', line)]
			lcsc = numbers[0]
			
			rows = df[df['lcsc'] == lcsc]
			if len(rows) == 0:
				no_stock = True
				print(f"Error: No Stock found for https://jlcpcb.com/partdetail/C{lcsc}")
			
		elif '(property "Stock"' in line and no_stock == True:
			lines[i] = f'		(property "Stock" "0"\n'
			
	with open(filename, "w") as file:
		file.writelines(lines)
		return
