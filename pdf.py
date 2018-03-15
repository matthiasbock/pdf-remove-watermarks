#!/usr/bin/python

from shlex import split
from subprocess import Popen, PIPE
from glob import glob

#
# Burst PDF into single pages
#
def pdf_burst(filename):
    cmd = "pdftk \""+filename+"\" burst"
    print cmd
    Popen(split(cmd)).wait()
    files = glob("pg_????.pdf")
    return sorted(files)

#
# Merge PDF pages into single PDF
#
def pdf_merge(pages, filename):
    cmd = "pdftk \""+"\" \"".join(pages)+"\" cat output \""+filename+"\""
    print cmd
    Popen(split(cmd)).wait()

#
# Convert PDF page to Scalable Vector Graphics (SVG)
#
def pdf_to_svg(pdf_filename, svg_filename):
    cmd = "inkscape --without-gui \""+pdf_filename+"\" --export-area-page --export-plain-svg=\""+svg_filename+"\""
    print cmd
    Popen(split(cmd)).wait()

#
# Convert SVG to PDF page
#
def svg_to_pdf(svg_filename, pdf_filename):
    cmd = "inkscape --without-gui \""+svg_filename+"\" --export-area-page --export-pdf=\""+pdf_filename+"\""
    print cmd
    Popen(split(cmd)).wait()
