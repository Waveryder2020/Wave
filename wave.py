#!/usr/bin/env python3

import sys
import pathlib
import json

sp = " " * 4
html_body = ""

p_title = "Wave Document"
p_bgcolor = "white"
p_bgimage = "none"
p_align = "left"
p_box = 0
p_box_style = "hidden"

def key_exists(dict_key, dictionary):
    keys = list(dictionary.keys())
    return (dict_key in keys)

def starts_with(long_str, sub_str):
    return (sub_str == long_str[0:len(sub_str)])

if len(sys.argv) == 1:
    path = input("Specify the path to the script: ")
else:
    path = sys.argv[1]

if pathlib.Path(path).exists():
    script_file = open(path, "r", encoding = "utf-8")
else:
    print(f"Invalid Path: {path}")
    exit()

script = json.load(script_file)
script_file.close()

if key_exists("~page", script):
    page_property = script["~page"]

    if key_exists("~title", page_property):
        p_title = page_property["~title"]
    if key_exists("~bg", page_property):
        p_bgcolor = page_property["~bg"]
    if key_exists("~img", page_property):
        p_bgimage = page_property["~img"]
    if key_exists("~align", page_property):
        p_align = page_property["~align"]
    if key_exists("~box", page_property):
        p_box = page_property["~box"]
    if key_exists("~box-style", page_property):
        p_box_style = page_property["~box-style"]

c_p_bgcolor = p_bgcolor
c_p_align = p_align
c_p_color = "black"
c_p_size = 17
c_p_box = 0
c_p_body = ""
c_p_points_type = "bullet"
c_p_points = ["*", "**", "***"]

def set_defaults():
    global c_p_bgcolor, c_p_align, c_p_color, c_p_size, c_p_box, c_p_body, c_p_points_type, c_p_points
    c_p_bgcolor = p_bgcolor
    c_p_align = p_align
    c_p_color = "black"
    c_p_size = 17
    c_p_box = 0
    c_p_body = ""
    c_p_points_type = "bullet"
    c_p_points = ["*", "**", "***"]

if key_exists("$content", script):
    content_property = script["$content"]

    if key_exists("$heading", content_property):
        heading = content_property["$heading"]
        html_body += f"\t<br><h1 style = 'text-align: center; font-family: Arial Narrow, sans-serif'>{heading}</h1>\n"
    if key_exists("$author", content_property):
        author = content_property["$author"]
        html_body += f"\t<br><h2 style = 'text-align: center; font-family: URW Chancery L, cursive'><i>{author}</i></h2>\n"

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
                if inherit == "default":
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
                if key_exists("!points-type", inherit):
                    if inherit["!type"] == "bullet":
                        pass
                if key_exists("$points-list", inherit):
                    c_p_points = inherit["$list"]
                    points_body = ""
                    for join_points in range(0, len(c_p_points)):
                        points_body += f"<li>{c_p_points[join_points]}</li>\n"
                    c_p_point_start = f"<ul style = 'text-align: {c_p_align}'>"
                    c_p_point_end = "</ul>"

        if starts_with(regular_keywords[keywords], "$text"):
            html_body += f"\t<p style = 'color: {c_p_color}; background-color: {c_p_bgcolor}; font-size: {c_p_size}px; text-align: {c_p_align}; margin: {c_p_box}px;'>{regular_values[keywords]}</p>\n"

        if starts_with(regular_keywords[keywords], "$points"):
            html_body += f"\t{c_p_point_start}{points_body}{c_p_point_end}\n"
        print(regular_keywords[keywords])
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

html_document = html_top + f"\n{sp}<body>\n\n" + html_body + f"\n{sp}</body>\n</html>\n"
file_name = path.split(".")
out_name = file_name[0] + ".html"
print(html_document)
out_file = open(out_name, "w+", encoding = "utf-8")
out_file.write(html_document)
out_file.close()
