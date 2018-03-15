#!/usr/bin/python

from sys import argv
from os import remove

from pdf import *

#
# Remove "Hitachi Displays Confidential" watermark
#
def remove_path(filename):
    svg = open(filename).read()

    output = svg
    cursor = 0
    start_marker = "<path"
    stop_marker = "/>"
    target1 = 'fill:#c0c0c0;'
    target2 = 'stroke:#c0c0c0;'
    found = False
    while (svg.find(start_marker, cursor) > -1):
        start = svg.find(start_marker, cursor)
        stop = svg.find(stop_marker, start) + len(stop_marker)
        text = svg[start:stop]
        if (text.find(target1) > -1) or (text.find(target2) > -1):
            spaces = (stop - start + 1) * " "
            temp = svg[:start] + spaces + svg[stop:]
            svg = temp
            print "FOUND"
            found = True
        cursor = stop

    if not found:
        print "NOT FOUND"

    open(filename, "w").write(svg)

#
# Main program
#
if __name__ == "__main__":
    if len(argv) < 2:
        print "Usage: " + argv[0] + " <filename.pdf>"
        exit()

    pages = pdf_burst(argv[1])
    print pages

    # page by page
    for pdf_filename in pages:
        # convert to SVG
        svg_filename = pdf_filename[:-4] + ".svg"
        pdf_to_svg(pdf_filename, svg_filename)
        # remove watermark
        remove_path(svg_filename)
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
