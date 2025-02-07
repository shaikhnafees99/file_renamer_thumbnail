import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["tkinter", "os"],
    "excludes": [],
    "include_files": []
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="FileRenamer",
    version="1.0",
    description="File Renaming Application",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base, icon=None)]
)