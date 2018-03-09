#!/usr/bin/python

from sys import argv
from os import remove

from common import *

def remove_watermark(filename):
    svg = open(filename).read()

    # Select last group in SVG = paths forming the text "OBSOLETE"
    start_marker = "<g"
    stop_marker = "</g></g></g></g></svg>"

    # Resolve recursive grouping
    start = -1
    for r in range(8):
        _start = svg[:start].rfind(start_marker)
        if _start < 0:
            print "Not found."
            return
        start = _start
    stop =  svg.find(stop_marker, start+1)
    if start < 0 or stop <= start:
        print "Not found."
        return
    print "Found."

    # output without this text
    new_svg = svg[:start] + svg[stop:]
    open(filename, "w").write(new_svg)

#
# Main program
#
if __name__ == "__main__":
    if len(argv) < 2:
        print "Usage: "+argv[0]+" <filename.pdf>"
        exit()

    pages = pdf_burst(argv[1])
    print pages

    # page by page
    for pdf_filename in pages:
        # convert to SVG
        svg_filename = pdf_filename[:-4]+".svg"
        pdf_to_svg(pdf_filename, svg_filename)
        # remove watermarks
        remove_watermark(svg_filename)
        # convert back to PDF
        svg_to_pdf(svg_filename, pdf_filename)
        # remove temporary SVG
        if (svg_filename[-4:] == ".svg"):
            remove(svg_filename)

    pdf_merge(pages, "output.pdf")
    
    # clean up
    for pdf_filename in pages:
        if (pdf_filename[-4:] == ".pdf"):
            remove(pdf_filename)
