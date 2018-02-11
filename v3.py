import sys, re

infile = open(sys.argv[1])
outfile = open('dump.txt', 'w')
for line in infile:
    if line.startswith('Cisco AP Name'):
        ap = line
    if line.lstrip().startswith('Radio Type'):
        radio = line
    if line.lstrip().startswith('External Antenna Gain'):
        gain = line
        output = ap + radio + gain
        outfile.write(output)
