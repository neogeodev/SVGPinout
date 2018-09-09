# SVGPinout
Generates a .svg pinout from a .csv file

Usage: svgpinout [pinout.csv | all]

First chip CSV line: Chip name, output file name, package, logo file name
All other lines: Pin name, Type, Direction (IN, OUT, BIDIR, or nothing)

See packages.csv

Type: 
* A=Address
* C=Control
* D=Data
* G=Graphics
* K=Clock
* M=Multiplexed
* P=Power (*GND and *VCC are colored automatically)
* ? or nothing=Unknown
