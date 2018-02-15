import sys
from cx_Freeze import setup , Executable

include_file = ['autorun.inf']
base = none
if sys.platform = "win32":
    base = None

setup(name = "Data_Extractor" ,
      version = "0.1" ,
      description = "Exacts_Data" ,
      options = {'build_exe':{'include_files':include_file}},
      executables = [Executable("scrapApp.py",base = base)])