# SVG pinout generator 0.11
# furrtek 09/2018
# Some chip package types are not tested !
# python -m pip install "cairosvg<2.0"

# Usage: svgpinout pinout.csv
# First CSV line: Chip name, Output file name, Package, Logo file name
# All other lines: Pin name, Type, Direction (IN, OUT, BIDIR)
# Type: A=Address, C=Control, D=Data, G=Graphics, K=Clock, M=Multiplexed, P=Power

import sys
import os
import svgwrite
import csv

# Edit this if needed:
pin_width = 20
pin_length = 80
font_size = 16
corner_margin = 40

packages = []
svg_document = 0
arrow_length = pin_width / 2
arrow_insert = []
arrow_rotation = 0

def arrow(direction):
	arrow = ""
	if direction == "OUT":
		# >
		arrow = "M " + str(arrow_insert[0]) + "," + str(arrow_insert[1])
		arrow += " l " + str(arrow_length) + "," + str(arrow_length)
		arrow += " l " + str(-arrow_length) + "," + str(arrow_length) + " z"
	elif direction == "IN":
		# <
		arrow = "M " + str(arrow_insert[0] + arrow_length) + "," + str(arrow_insert[1])
		arrow += " l " + str(-arrow_length) + "," + str(arrow_length)
		arrow += " l " + str(arrow_length) + "," + str(arrow_length) + " z"

	if arrow != "":
		svg_document.add(svg_document.path(d = arrow,
							           fill="black",
							           transform = arrow_rotation,
		                               stroke_width = "1",
		                               stroke = "black"))

def generate(filename):
    global svg_document
    global arrow_insert
    global arrow_rotation
    
    rows = []
    pincount = 0
    pin_total = 0
    pincount_w = 0
    pincount_h = 0
    ref_size = 0
    dot_size = 0
    edge = 0		# Start with bottom edge
    pin_counter = 0
    
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        for row in csv_reader:
            rows.append(row)
    
    chip_name = rows[0][0]
    svg_file_name = "./svg/" + rows[0][1] + ".svg"
    logo_file_name = rows[0][3]
    print("Drawing chip " + chip_name + " (" + svg_file_name + ")...")
    
    # Look for package definition
    for package in packages:
        if package[0] == rows[0][2]:
            pincount = int(package[1])
            pincount_w = int(package[2])
            pincount_h = int(package[3])
            pin_number = int(package[4])
            ref_size = int(package[5])
            dot_size = int(package[6])
            chip_h = int(package[7])	# DIP height, overwritten for quad packages
            pin_space = pin_width * float(package[8])
            break
    
    if dot_size == 0:
        print("Unsupported package: " + rows[0][2])
        exit()

    # Chip case width and height
    chip_w = pincount_w * pin_width + (pincount_w-1) * pin_space + corner_margin*2
    if (pincount_h != 0):
        chip_h = pincount_h * pin_width + (pincount_h-1) * pin_space + corner_margin*2

    # SVG document width and height
    if (pincount_h != 0):
        doc_w = chip_w + pin_length*2 + arrow_length*2
        chip_x = pin_length + arrow_length
    else:
        doc_w = chip_w
        chip_x = 0
    doc_h = chip_h + pin_length*2 + arrow_length*2
    svg_document = svgwrite.Drawing(filename = svg_file_name, size = (str(doc_w) + "px", str(doc_h) + "px"))

    # Chip package background
    svg_document.add(svg_document.rect(insert = (chip_x, arrow_length + pin_length),
                                       size = (str(chip_w) + "px", str(chip_h) + "px"),
                                       stroke = "none",
                                       fill = "white"))

    markings_x = chip_x + chip_w * 0.2
    markings_y = pin_length + arrow_length + chip_h * 0.1

    # Logo, if present
    if logo_file_name != "":
        svg_document.add(svg_document.image("../logos/" + logo_file_name,
            									size = (chip_w * 0.4, chip_h * 0.4),
                                                insert = (markings_x, markings_y)))
    markings_y += 30 + (doc_h * 0.25)

    # Chip name
    svg_document.add(svg_document.text(chip_name,
                                        fill = "black",
                                        style = "font-size:" + str(ref_size) + "px; font-family:Verdana;",
                                        insert = (markings_x, markings_y)))

    # Pin 1 marker
    svg_document.add(svg_document.circle(r=str(dot_size),
    fill = "none",
    stroke_width = "1",
    stroke = "black",
    center = (chip_x + (dot_size * 3), doc_h - (pin_length + (dot_size * 3)))))
    
    for i in range(1, len(rows)):
        if rows[i] == []:
        	continue
        pin = rows[i]
        pin_name = pin[0]
        if len(pin) > 1:
            pin_type = pin[1]
        else:
            pin_type = '?'
        
        # Color decode
        if pin_type == "A":
            rgb_color = "rgb(255,255,127)"
        elif pin_type == "C":
            rgb_color = "rgb(159,127,223)"
        elif pin_type == "D":
            rgb_color = "rgb(127,191,255)"
        elif pin_type == "G":
            rgb_color = "rgb(159,191,127)"
        elif pin_type == "I":
            rgb_color = "rgb(0,255,191)"
        elif pin_type == "K":
            rgb_color = "rgb(255,0,255)"
        elif pin_type == "M":
            rgb_color = "rgb(255,127,0)"
        elif pin_type == "O":
            rgb_color = "rgb(0,159,127)"
        elif pin_type == "P":
            if "VCC" in pin_name:
                rgb_color = "rgb(255,0,0)"
            elif "GND" in pin_name:
                rgb_color = "rgb(127,127,127)"
        else:
            rgb_color = "rgb(255,255,255)"
        
        centering = pin_length/2 - len(pin_name) * 4.8
        number_length = len(str(pin_number)) * 4.8

        corner_offset = chip_x + corner_margin
        bottom_offset = chip_x + chip_h - corner_margin - pin_width
        right_offset = chip_x + chip_w - corner_margin - pin_width
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
            number_insert = (pin_insert[0] - number_length + 10, pin_insert[1] + pin_length + 20)
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

        if (pin_number == pincount):
            pin_number = 1
        else:
            pin_number += 1
    
        # Progress along chip edges
        pin_total += 1
        pin_counter += 1
        if (edge == 0) and (pin_counter == pincount_w):
            pin_counter = 0
            if (pincount_h > 0):
                edge = 1	# Quad
            else:
                edge = 2    # Dual
        elif (edge == 1) and (pin_counter == pincount_h):
            pin_counter = 0
            edge = 2
        elif (edge == 2) and (pin_counter == pincount_w):
            pin_counter = 0
            edge = 3
    
    if pin_total != pincount:
        print("Error: pin count is incorrect ! Got " + str(pin_total) + " need " + str(pincount))
        exit()

    # Chip package outline
    svg_document.add(svg_document.rect(insert = (chip_x, arrow_length + pin_length),
                                       size = (str(chip_w) + "px", str(chip_h) + "px"),
                                       stroke_width = "1",
                                       stroke = "black",
                                       fill = "none"))
    svg_document.save()
                
if len(sys.argv) != 2:
	print("Usage: svgpinout [pinout.csv | all]")
	exit()
else:
	# Load package definitions
	with open("packages.csv") as package_file:
	    package_reader = csv.reader(package_file, delimiter = ',')
	    next(package_reader)
	    for row in package_reader:
	    	packages.append(row)
	    print("Loaded " + str(len(packages)) + " package definitions.")

	if (sys.argv[1] == "all"):
		for file in os.listdir("./csv/"):
		    if file.endswith(".csv"):
		        generate("./csv/" + file)
	else:
		generate(sys.argv[1])

	print("Done !")
