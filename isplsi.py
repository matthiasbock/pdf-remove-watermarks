#!/usr/bin/python

from shlex import split
from subprocess import Popen, PIPE
from glob import glob
from os import remove

def pdf_burst(filename):
    cmd = "pdftk \""+filename+"\" burst"
    print cmd
    Popen(split(cmd)).wait()
    files = glob("pg_????.pdf")
    return sorted(files)

def pdf_merge(pages, filename):
    cmd = "pdftk \""+"\" \"".join(pages)+"\" cat output \""+filename+"\""
    print cmd
    Popen(split(cmd)).wait()

def pdf_to_svg(pdf_filename, svg_filename):
    cmd = "inkscape --without-gui \""+pdf_filename+"\" --export-area-page --export-plain-svg=\""+svg_filename+"\""
    print cmd
    Popen(split(cmd)).wait()

def svg_to_pdf(svg_filename, pdf_filename):
    cmd = "inkscape --without-gui \""+svg_filename+"\" --export-area-page --export-pdf=\""+pdf_filename+"\""
    print cmd
    Popen(split(cmd)).wait()

def remove_all_devices_discontinued(filename):
    svg = open(filename).read()

    output = svg
    cursor = 0
    start_marker = "<text"
    stop_marker = "</text>"
    target1 = "ALL DEVICES"
    target2 = "DISCONTINUED"
    while (svg.find(start_marker, cursor) > -1):
        start = svg.find(start_marker, cursor)
        stop =  svg.find(stop_marker, start) + len(stop_marker)
        text = svg[start:stop]
        if (text.find(target1) > -1) and (text.find(target2) > -1):
            # output without this text
            output = svg[:start] + svg[stop:]
            print "FOUND"
            break
        cursor = stop

    open(filename, "w").write(output)

if __name__ == "__main__":
    pages = pdf_burst("ispLSI1016DataSheet.PDF")
    print pages

    # page by page
    for pdf_filename in pages:
        # convert to SVG
        svg_filename = pdf_filename[:-4]+".svg"
        pdf_to_svg(pdf_filename, svg_filename)
        # remove watermark
        remove_all_devices_discontinued(svg_filename)
        # convert back to PDF
        svg_to_pdf(svg_filename, pdf_filename)
        # remove temporary SVG
        remove(svg_filename)

    pdf_merge(pages, "output.pdf")
    
    # clean up
    for pdf_filename in pages:
        remove(pdf_filename)
