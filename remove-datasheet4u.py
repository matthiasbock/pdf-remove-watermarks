#!/usr/bin/python

from sys import argv
from os import remove

from pdf import *
from filter import *


def remove_watermarks(filename):
    svg = open(filename).read()

    svg = filter_out_element(
                svg,
                "<text",
                "</text>",
                "www.DataSheet4U.com"
                )

    svg = filter_out_element(
                svg,
                "<image",
                "/>",
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOYAAABsCAYAAAB+Qc4FAAAABHNCSVQICAgIfAhkiAAAIABJREFUeJzsvXe4ZUd19vmrqr1PDjfnezv3bXWO"
                )

    svg = filter_out_element(
                svg,
                "<image",
                "/>",
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAKoAAAAbCAYAAADs4BRSAAAABHNCSVQICAgIfAhkiAAACzlJREFUeJztW9ly5LYOBUVJ3XJ7Gddk/v/rkqpMHNu9aC"
                )

    open(filename, "w").write(svg)


#
# Main program
#
if __name__ == "__main__":
    if len(argv) < 2:
        print "Usage: " + argv[0] + " <filename.pdf>"
        exit()

    # Split PDF
    pages = pdf_burst(argv[1])
    print pages

    # Process page by page
    for pdf_filename in pages:
        # Convert to SVG
        svg_filename = pdf_filename[:-4] + ".svg"
        pdf_to_svg(pdf_filename, svg_filename)
        # Remove watermarks
        remove_watermarks(svg_filename)
        # Convert back to PDF
        svg_to_pdf(svg_filename, pdf_filename)
        # Remove temporary SVG
        if (svg_filename[-4:] == ".svg"):
            remove(svg_filename)

    # Re-assemble PDF
    pdf_merge(pages, "output.pdf")

    # Clean up
    for pdf_filename in pages:
        if (pdf_filename[-4:] == ".pdf"):
            remove(pdf_filename)
