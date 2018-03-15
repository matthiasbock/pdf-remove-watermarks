#!/usr/bin/python

from sys import argv
from os import remove

from pdf import *

def remove_watermarks(filename):
    svg = open(filename).read()

    cursor = 0
    start_marker = "<text"
    stop_marker = "</text>"
    target1 = "MEDIATEK CONFIDENTIAL"
    target2 = "FOR chunping.miao@ nbbsw.com USE ONLY"
    while (svg.find(start_marker, cursor) > -1):
        start = svg.find(start_marker, cursor)
        stop = svg.find(stop_marker, start) + len(stop_marker)
        text = svg[start:stop]
        if (text.find(target1) > -1) or (text.find(target2) > -1):
            # output without this text
            new_svg = svg[:start] + svg[stop:]
            svg = new_svg
            print "FOUND"
        cursor = start + 1

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
        # remove watermarks
        remove_watermarks(svg_filename)
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
