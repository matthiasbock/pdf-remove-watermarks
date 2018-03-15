#
# This file contains functions
# to filter out certain parts from file content
#

def filter_out_element(svg, start_marker, stop_marker, keyword):
    cursor = 0
    # Iterate over all matching tags
    while (svg.find(start_marker, cursor) > -1):
        start = svg.find(start_marker, cursor)
        stop = svg.find(stop_marker, start) + len(stop_marker)
        haystack = svg[start:stop]
        if (haystack.find(keyword) > -1):
            # Found keyword => Remove tag
            new_svg = svg[:start] + svg[stop:]
            svg = new_svg
            print "Keyword found"
        cursor = start + 1
    return svg
