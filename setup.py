import sys
from cx_Freeze import setup, Executable

# GUI applications require a different base on Windows (the default is for a console application).
base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

setup(
    name="PyPlatformer",
    version="0.7",
    description="My Final Project!",
    executables=[
        Executable("main.py", base=base),
    ],
    options={
        "build_exe": {
            "optimize": 2,
            "includes": ["pygame"],
            "excludes": ["tkinter"],
            "include_files": ["./assets/"],
            "packages": [
                "enum", "os", "pygame", "math", "time", "sys",
            ],
        },
    },
)
