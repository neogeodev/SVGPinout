# SVGPinout
Generates a .svg pinout from a .csv file

Usage: svgpinout [pinout.csv | all]

First CSV line: Chip name

Second CSV line: Package (see script for list)

All other lines: Pin name, Type, Direction (IN, OUT, BIDIR, or nothing)

Type: 
* A=Address
* C=Control
* D=Data
* G=Graphics
* K=Clock
* M=Multiplexed
* P=Power
* ? or nothing=Unknown
