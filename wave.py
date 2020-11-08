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

if key_exists("$content", script):
    content_property = script["$content"]

    if key_exists("$heading", content_property):
        heading = content_property["$heading"]
        html_body += f"\t<br><h1 style = 'text-align: center; font-family: Arial Narrow, sans-serif'>{heading}</h1>\n"
    if key_exists("$author", content_property):
        author = content_property["$author"]
        html_body += f"\t<br><h2 style = 'text-align: center; font-family: URW Chancery L, cursive'><i>{author}</i></h2>\n"

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
                margin-top: {p_box}px;
                margin-left: {p_box}px;
                margin-right: {p_box}px;
                margin-bottom: {p_box}px;
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
