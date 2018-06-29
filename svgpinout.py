# SVG pinout generator 0.1
# furrtek 06/2018
# Only QFPR*, QFP160 packages have been tested !

# Usage: svgpinout pinout.csv
# First CSV line: Chip name
# Second CSV line: Package
# All other lines: Pin name, Type, Direction (IN, OUT, BIDIR)
# Type: A=Address, C=Control, D=Data, G=Graphics, K=Clock, M=Multiplexed, P=Power

import sys
import svgwrite
import csv

# Edit this if needed:
pin_width = 20
pin_space = 10
pin_length = 80
font_size = 16
corner_margin = 40

rows = []
pincount_w = 0
pincount_h = 0
edge = 0		# Start with bottom edge
pin_counter = 0
arrow_length = pin_width / 2

def arrow(direction):
	if direction == "OUT":
		arrow = "M " + str(arrow_insert[0]) + "," + str(arrow_insert[1])
		arrow += " l " + str(arrow_length) + "," + str(arrow_length)
		arrow += " l " + str(-arrow_length) + "," + str(arrow_length) + " z"
	elif direction == "IN":
		arrow = "M " + str(arrow_insert[0] + arrow_length) + "," + str(arrow_insert[1])
		arrow += " l " + str(-arrow_length) + "," + str(arrow_length)
		arrow += " l " + str(arrow_length) + "," + str(arrow_length) + " z"

	svg_document.add(svg_document.path(d = arrow,
							           fill="black",
							           transform = arrow_rotation,
		                               stroke_width = "1",
		                               stroke = "black"))

if len(sys.argv) != 2:
	print("Usage: svgpinout pinout.csv")
	exit()

with open(sys.argv[1]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    for row in csv_reader:
    	rows.append(row)

    chip_name = rows[0][0]
    print(chip_name)

    package = rows[1][0]
    if package == "SOIC24":
    	pincount_w = 12
    	ref_size = 50
    	dot_size = 30
    elif package == "QFP48":
    	pincount_w = 12
    	pincount_h = 12
    	ref_size = 50
    	dot_size = 30
    elif package == "SDIP64":
    	pincount_w = 32
    	ref_size = 50
    	dot_size = 30
    elif package == "QFPR64":
    	pincount_w = 19
    	pincount_h = 13
    	ref_size = 50
    	dot_size = 30
    elif package == "QFPR80":
    	pincount_w = 24
    	pincount_h = 16
    	ref_size = 60
    	dot_size = 30
    elif package == "QFPR100":
    	pincount_w = 30
    	pincount_h = 20
    	ref_size = 70
    	dot_size = 40
    elif package == "QFP120":
    	pincount_w = 30
    	pincount_h = 30
    	ref_size = 50
    	dot_size = 30
    elif package == "QFP136":
    	pincount_w = 34
    	pincount_h = 34
    	ref_size = 50
    	dot_size = 30
    elif package == "QFP160":
    	pincount_w = 40
    	pincount_h = 40
    	ref_size = 90
    	dot_size = 50
    elif package == "QFP176":
    	pincount_w = 44
    	pincount_h = 44
    	ref_size = 50
    	dot_size = 30
    elif package == "QFP208":
    	pincount_w = 52
    	pincount_h = 52
    	ref_size = 50
    	dot_size = 30
    else:
    	print("Unsupported package: " + package)
    	exit()

    chip_w = pincount_w * pin_width + (pincount_w-1) * pin_space + corner_margin*2
    chip_h = pincount_h * pin_width + (pincount_h-1) * pin_space + corner_margin*2

    doc_w = chip_w + pin_length*2 + arrow_length*2
    doc_h = chip_h + pin_length*2 + arrow_length*2
    svg_document = svgwrite.Drawing(filename = chip_name + ".svg", size = (str(doc_w) + "px", str(doc_h) + "px"))

    svg_document.add(svg_document.image("logo_snk.png",
    									size = (doc_w * 0.3, doc_h * 0.3),
										insert = (doc_w * 0.2, doc_h * 0.15)))

    svg_document.add(svg_document.text(chip_name,
									   fill = "black",
									   style = "font-size:" + str(ref_size) + "px; font-family:Verdana;",
	                                   insert = (doc_w * 0.2, doc_h * 0.2 + 180)))

    # Pin 1 marker
    svg_document.add(svg_document.circle(r=str(dot_size),
									   fill = "none",
	                                   stroke_width = "1",
									   stroke = "black",
	                                   center = (pin_length + (dot_size * 3), doc_h - (pin_length + (dot_size * 3)))))

    for i in range(2, len(rows)):
		pin = rows[i]
		pin_name = pin[0]
		if len(pin) > 1:
			pin_type = pin[1]
		else:
			pin_type = '?'
		pin_number = i - 1

		# Color decode
		if pin_type == "A":
			rgb_color = "rgb(255,255,127)"
		elif pin_type == "C":
			rgb_color = "rgb(159,127,223)"
		elif pin_type == "D":
			rgb_color = "rgb(127,191,255)"
		elif pin_type == "G":
			rgb_color = "rgb(159,191,127)"
		elif pin_type == "K":
			rgb_color = "rgb(255,0,255)"
		elif pin_type == "M":
			rgb_color = "rgb(255,127,0)"
		elif pin_type == "P":
			if pin_name == "VCC":
				rgb_color = "rgb(255,0,0)"
			elif pin_name == "GND":
				rgb_color = "rgb(127,127,127)"
		else:
			rgb_color = "rgb(255,255,255)"

		centering = pin_length/2 - len(pin_name) * 4.8
		number_length = len(str(pin_number)) * 4.8

		corner_offset = arrow_length + pin_length + corner_margin
		bottom_offset = arrow_length + pin_length + chip_h - corner_margin - pin_width
		right_offset = arrow_length + pin_length + chip_w - corner_margin - pin_width
		pin_offset = pin_counter * (pin_width + pin_space)

		if (edge == 0):
			pin_insert = (corner_offset + pin_offset, chip_h + pin_length + arrow_length)
			text_insert = (-pin_insert[1] - pin_length + centering, pin_insert[0] + 15.5)
			number_insert = (pin_insert[0] + 10 - number_length, pin_insert[1] - 10)
			arrow_insert = (pin_insert[1] + pin_length, -pin_insert[0] - pin_width)
			pin_size = (str(pin_width) + "px", str(pin_length) + "px")
			text_rotation = "rotate(-90)"
			arrow_rotation = "rotate(90)"
		elif (edge == 1):
			pin_insert = (chip_w + pin_length + arrow_length, bottom_offset - pin_offset)
			text_insert = (pin_insert[0] + centering, pin_insert[1] + 15.5)
			number_insert = (pin_insert[0] - 10 - number_length*2, pin_insert[1] + 15.5)
			arrow_insert = (pin_insert[0] + pin_length, pin_insert[1])
			pin_size = (str(pin_length) + "px", str(pin_width) + "px")
			text_rotation = "rotate(0)"
			arrow_rotation = "rotate(0)"
		elif (edge == 2):
			pin_insert = (right_offset - pin_offset, arrow_length)
			text_insert = (-pin_insert[1] - pin_length + centering, pin_insert[0] + 15.5)
			number_insert = (pin_insert[0], pin_insert[1] + pin_length + 20)
			arrow_insert = (-arrow_length, pin_insert[0])
			pin_size = (str(pin_width) + "px", str(pin_length) + "px")
			text_rotation = "rotate(-90)"
			arrow_rotation = "rotate(-90)"
		elif (edge == 3):
			pin_insert = (arrow_length, corner_offset + pin_offset)
			text_insert = (pin_insert[0] + centering, pin_insert[1] + 15.5)
			number_insert = (pin_insert[0] + 10 + pin_length, pin_insert[1] + 15.5)
			arrow_insert = (-arrow_length, -pin_insert[1] - pin_width)
			pin_size = (str(pin_length) + "px", str(pin_width) + "px")
			text_rotation = "rotate(0)"
			arrow_rotation = "rotate(180)"

		# Pin number
		svg_document.add(svg_document.text(str(pin_number),
										   fill = "black",
										   style = "font-size:" + str(font_size) + "px; font-family:Bitstream Vera Sans Mono;",
		                                   insert = number_insert))

		# Pin outline
		if pin_name == "NC":
			svg_document.add(svg_document.rect(insert = pin_insert,
			                                   size = pin_size,
			                                   stroke_width = "1",
			                                   stroke = "grey",
			                                   stroke_dasharray = "5,5",
			                                   fill = "white"))
		else:
			svg_document.add(svg_document.rect(insert = pin_insert,
			                                   size = pin_size,
			                                   stroke_width = "1",
			                                   stroke = "black",
			                                   fill = rgb_color))
	
		# Pin name
		svg_document.add(svg_document.text(pin_name,
										   fill = "black",
										   style = "font-size:" + str(font_size) + "px; font-family:Bitstream Vera Sans Mono;",
										   transform = text_rotation,
		                                   insert = text_insert))
		
		# Direction arrow
		if len(pin) > 2:
			if pin[2] == "BIDIR":
				arrow("IN")
				arrow("OUT")
			else:
				arrow(pin[2])

		# Progress along chip edges
		pin_counter += 1
		if (edge == 0) and (pin_counter == pincount_w):
			pin_counter = 0
			if (pincount_h > 0):
				edge = 1
			else:
				edge = 2
		elif (edge == 1) and (pin_counter == pincount_h):
			pin_counter = 0
			edge = 2
		elif (edge == 2) and (pin_counter == pincount_w):
			pin_counter = 0
			edge = 3

    # Chip outline
    svg_document.add(svg_document.rect(insert = (arrow_length + pin_length, arrow_length + pin_length),
	                                   size = (str(chip_w) + "px", str(chip_h) + "px"),
	                                   stroke_width = "1",
	                                   stroke = "black",
	                                   fill = "none"))

print("Done !")

svg_document.save()
