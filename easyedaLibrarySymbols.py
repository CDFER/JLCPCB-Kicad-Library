# easyedaLibrarySymbols.py

class Args:
    def __init__(self):
        self.footprint_creation = True
        self.symbol_creation = True
        self.footprint_lib = "JLCPCB-Kicad-Footprints"
        self.output_dir = "JLC2KiCad_lib"
        self.model_base_variable = ""
        self.model_dir = "3dModels"
        self.models = ["STEP"]
        self.skip_existing = False
        self.symbol_lib = "JLCPCB-ICs"
        self.symbol_lib_dir = "JLCPCB-Kicad-Symbols"

args = Args()

def generateEasyEdaLibrary(componentList):
    for component in componentList:
        JLC.add_component(f"C{component}", args)
        
    return