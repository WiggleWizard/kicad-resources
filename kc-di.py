# KiCAD Dual Inliner
# ------------------
# Dual Inline schematic generator for KiCAD.
# 
# Author: Terence-Lee 'Zinglish' Davis


HEADER = """EESchema-LIBRARY Version 2.3
#encoding utf-8
#
# %s
#
DEF %s U 0 40 Y Y 1 F N
F1 "%s" %d %d 50 H V C CNN
F0 "U" %d %d 50 H V C CNN
DRAW"""
PIN_META = "\nX %s %d %d %d %d %s 50 50 1 1 U"
DRAW_META = "\nS %i %i %i %i 0 1 0 N"
FOOTER = """
ENDDRAW
ENDDEF
#
#End Library"""
PIN_LENGTH = 300


#===================================================================
# START PROGRAM
#===================================================================
import sys

usage = "Usage: kc-di pinout_path output_path schematic_name"

# If CLI params don't match
if len(sys.argv) != 4:
	print(usage)
	exit()

# Pull out CLI params
pinout_path = sys.argv[1]
output_path = sys.argv[2]
symbol_name = sys.argv[3]

SYMBOL_WIDTH = 2500
SYMBOL_PITCH = 100

f = None
try:
	f = open(pinout_path)
except(IOError):
	print("No pinout file found or no permission to read (" + pinout_path + ")")
	exit()

sys.stdout.write("Reading pinout file")

total_length = 0 # Total length of the symbol

# Read the pinout file line by line
pins = ""
content = f.readlines()
for i in range(0, len(content)):
	l = content[i].strip("\n")
	s = l.split(",")

	if s[0] == "":
		s[0] = 0

	pin_number = int(s[0])
	pin_name   = s[1]
	pin_side   = i % 2

	pin_orientation = 'R'
	if pin_side == 1:
		pin_orientation = 'L'
		total_length = total_length + SYMBOL_PITCH

	x = pin_side * SYMBOL_WIDTH
	y = (i - pin_side) / 2 * SYMBOL_PITCH

	if s[1] == "":
		continue

	pins += PIN_META % (pin_name, pin_number, x, -y, PIN_LENGTH, pin_orientation)

	sys.stdout.write(".")

f.close()

sys.stdout.write("complete\n")

# Add symbol boundary
pins += DRAW_META % (PIN_LENGTH, SYMBOL_PITCH, SYMBOL_WIDTH - PIN_LENGTH, -total_length - SYMBOL_PITCH)

# Add labels and other data to header
header = HEADER % (symbol_name, symbol_name, symbol_name, SYMBOL_WIDTH / 2, -total_length / 2,  SYMBOL_WIDTH / 2, -total_length / 2 + 100)

# Add header and footer
output = header + pins + FOOTER

try:
	f = open(output_path, 'w')
except(IOError):
	print("Error attempting to open output path for writing (" + output_path + ")")
	exit()

f.truncate()
f.write(output)
f.close()

print("Done!")