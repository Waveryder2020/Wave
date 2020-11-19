#!/usr/bin/env python3

import sys
import pathlib
import json

sp = " " * 4
html_body = ""

# Default properties for the ~page container.
p_title = "Wave Document"
p_bgcolor = "white"
p_bgimage = "none"
p_align = "left"
p_box = 0
p_box_style = "hidden"

def key_exists(dict_key, dictionary):
    """
        Checks if a key exists in a dictionary.
    """
    keys = list(dictionary.keys())
    return (dict_key in keys)

def starts_with(long_str, sub_str):
    """
        Checks if a string starts with another string.
    """
    return (sub_str == long_str[0:len(sub_str)])

"""
    Checks if the script file is passed as a command-line argument.
    If not, then asks the user to specify it.
"""
if len(sys.argv) == 1:
    path = input("Specify the path to the script: ")
else:
    path = sys.argv[1]

# Checks if the specified script path exists or not.
if pathlib.Path(path).exists():
    script_file = open(path, "r", encoding = "utf-8")
else:
    print(f"Invalid Path: {path}")
    exit()

# Converts JSON from script to a Python Dictionary.
script = json.load(script_file)
script_file.close()

if key_exists("~page", script):
    page_property = script["~page"]

    if key_exists("~title", page_property):
        p_title = page_property["~title"]
    if key_exists("~bg", page_property):
        p_bgcolor = page_property["~bg"]
    if key_exists("~pic", page_property):
        p_bgimage = page_property["~pic"]
    if key_exists("~align", page_property):
        p_align = page_property["~align"]
    if key_exists("~box", page_property):
        p_box = page_property["~box"]
    if key_exists("~box-style", page_property):
        p_box_style = page_property["~box-style"]

# Default properties for the $content container.
c_p_bgcolor = p_bgcolor
c_p_align = p_align
c_p_color = "black"
c_p_size = 17
c_p_box = 0
c_p_body = ""
c_p_points_type = "bullet"
c_p_point_start = "ul"

def set_defaults():
    """
        Sets all the $content properties to their default values.
    """
    global p_bg_color, p_align, c_p_bgcolor, c_p_align, c_p_color, \
        c_p_size, c_p_box, c_p_body, c_p_points_type, c_p_point_start
    c_p_bgcolor = p_bgcolor
    c_p_align = p_align
    c_p_color = "black"
    c_p_size = 17
    c_p_box = 0
    c_p_body = ""
    c_p_points_type = "bullet"
    c_p_point_start = "ul"

if key_exists("$content", script):
    content_property = script["$content"]

    if key_exists("$heading", content_property):
        heading = content_property["$heading"]
        html_body += ("\t<br>\n\t<h1 style = 'text-align: center;" + \
            f"font-family: Arial Narrow, sans-serif'>{heading}</h1>\n")
    if key_exists("$author", content_property):
        author = content_property["$author"]
        html_body += "\t<br>\n\t<h2 style = 'text-align: center;" + \
            f"font-family: URW Chancery L, cursive'><i>{author}</i></h2>\n"

    content_property_copy = content_property.copy()
    if key_exists("$heading", content_property_copy):
        del content_property_copy["$heading"]
    if key_exists("$heading", content_property_copy):
        del content_property_copy["$author"]
    regular_keywords = list(content_property_copy.keys())
    regular_values = list(content_property_copy.values())

    for keywords in range(0, len(regular_keywords)):
        if starts_with(regular_keywords[keywords], "!inherit"):
            inherit = content_property[regular_keywords[keywords]]

            if isinstance(inherit, str):
                if inherit == "!default":
                    set_defaults()
                else:
                    pass
            elif isinstance(inherit, dict):
                if key_exists("!size", inherit):
                    c_p_size = inherit["!size"]
                if key_exists("!color", inherit):
                    c_p_color = inherit["!color"]
                if key_exists("!align", inherit):
                    c_p_align = inherit["!align"]
                if key_exists("!bg", inherit):
                    c_p_bgcolor = inherit["!bg"]
                if key_exists("!box", inherit):
                    c_p_box = inherit["!box"]
                # if key_exists("!points-type", inherit):
                #     if inherit["!type"] == "bullet":
                #         pass


        if starts_with(regular_keywords[keywords], "$text"):
            html_body += (f"\t<p style = 'color: {c_p_color}; background-color: {c_p_bgcolor}; font-size:" + \
                f"{c_p_size}px; text-align: {c_p_align}; margin: {c_p_box}px;'>{regular_values[keywords]}</p>\n")

        if starts_with(regular_keywords[keywords], "$points"):
            points = regular_values[keywords]
            points_head = (f"\t<{c_p_point_start} style = 'color: {c_p_color}; background-color: {c_p_bgcolor}; font-size:" + \
                f"{c_p_size}px; text-align: {c_p_align}; margin: {c_p_box}px;'>\n")
            points_body = ""
            for c_p_points_join in range(0, len(points)):
                points_body += f"\t\t<li>{points[c_p_points_join]}</li>\n"
            points_complete = points_head + points_body + f"\t</{c_p_point_start}>\n"
            html_body += points_complete

        if starts_with(regular_keywords[keywords], "$pic"):
            html_body += f"\t<img 'color: {c_p_color}; background-color: {c_p_bgcolor}; font-size:" + \
                f"{c_p_size}px; text-align: {c_p_align}; margin: {c_p_box}px;' src = '{regular_values[keywords]}'>"

html_top = f"""
<!--
This Document is generated using Wave.
Wave: https://www.github.com/Waveryder2020/Wave
-->

<!DOCTYPE html>
<html>
    <head>
        <title>{p_title}</title>
        <style>
            body {{
                background-color: {p_bgcolor};
                background-image: url({p_bgimage});
                text-align: {p_align};
                margin: {p_box}px;
                border-style: {p_box_style};
            }}
        </style>
    </head>
"""

# Assembles the complete HTML Document.
html_document = html_top + f"\n{sp}<body>\n\n" + html_body + f"\n{sp}</body>\n</html>\n"

# Removes the script extension (if it exists) and adds .html extenstion.
file_name = path.split(".")
if len(file_name) == 1:
    file_name.append(".html")
else:
    file_name[-1] = ".html"

# Writes the HTML Document in a HTML file.
out_name = "".join(file_name)
print(html_document)
out_file = open(out_name, "w+", encoding = "utf-8")
out_file.write(html_document)
out_file.close()
print(f"Transpiled successfully to file: {out_name}")
