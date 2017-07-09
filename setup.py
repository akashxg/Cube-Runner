import os
os.environ['TCL_LIBRARY'] = "C:\\Users\\Akash\\AppData\\Local\\Programs\\Python\\Python36\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\Akash\\AppData\\Local\\Programs\\Python\\Python36\\tcl\\tk8.6"
import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
	version="22.99",
	name = "Cube Runner",
	options = {"build_exe": {"packages": ["pygame"],
							 "include_files":["assets\\images\\new_triangle.png"]}},
	executables = executables

	)