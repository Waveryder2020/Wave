#!/usr/bin/env python3

import sys
import pathlib
import json
import wave_lib as wl

p_title = "Wave Document"
p_bgcolor = "white"
p_bgimage = "none"
p_align = "left"
p_margin = 0

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

if wl.key_exists("~page", script):
    page_property = script["~page"]

if wl.key_exists("~title", page_property):
    p_title = page_property["~title"]
if wl.key_exists("~bg", page_property):
    p_bgcolor = page_property["~bg"]
if wl.key_exists("~img", page_property):
    p_bgimage = page_property["~img"]
if wl.key_exists("~align", page_property):
    p_align = page_property["~align"]
if wl.key_exists("~margin", page_property):
    p_margin = page_property["~margin"]

print(p_align); print(p_margin); print(p_bgcolor)

html_top = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>{p_title}</title>
        <style>
            body {{
                background-color: {p_bgcolor};
                background-image: url({p_bgimage});
                text-align: {p_align};
                margin-top: {p_margin}px;
                margin-left: {p_margin}px;
                margin-right: {p_margin}px;
                margin-bottom: {p_margin}px;
            }}
        </style>
    </head>
"""

document = html_top + "<body><p>Text</p></body></html>"
file = open("doc.html", "w+", encoding = "utf-8")
file.write(document)
file.close()
