#!/usr/bin/env python3

from jinja2 import Template
from ast import literal_eval
import json
from glob import glob
import os.path
import regex as re
from collections import OrderedDict

colon_re = re.compile(r"[:៖،,/]")

all_tags = [os.path.split(p)[1] for p in glob("cldr-misc-full/main/*")]

num_systems = {}
for code, num_sys in json.load(open("cldr-core/supplemental/numberingSystems.json"))["supplemental"]["numberingSystems"].items():
    try:
        num_systems[code] = num_sys["_digits"]
    except KeyError:
        continue

def get_data(tag):
    output = {}
    c_dict = json.load(open(f"cldr-misc-full/main/{tag}/characters.json"))
    c_string = c_dict["main"][tag]["characters"]["exemplarCharacters"]
    c_list = literal_eval(f"\"{c_string}\"").strip("[]").split(" ")
    characters = []
    for c in c_list:
        if c.startswith("{") and c.endswith("}"):
            characters.append(c[1:-1])
        elif len(c) == 3 and "-" in c:
            start, end = ord(c[0]), ord(c[-1])
            characters.extend([chr(cp) for cp in range(start, end + 1)])
        else:
            characters.append(c)      
    characters = [c.upper() for c in characters]
    characters = list(OrderedDict.fromkeys(characters))
    output["letters"] = ["".join(characters[i:i+13]) for i in range(0, len(characters), 13)]
    p_dict = json.load(open(f"cldr-misc-full/main/{tag}/posix.json"))
    p_messages = p_dict["main"][tag]["posix"]["messages"]
    output["yes"], output["no"] = colon_re.split(p_messages["yesstr"])[0].strip(), colon_re.split(p_messages["nostr"])[0].strip()
    n_dict = json.load(open(f"cldr-numbers-full/main/{tag}/numbers.json"))
    n_numbers = n_dict["main"][tag]["numbers"]
    num_sys_set = {n_numbers["defaultNumberingSystem"]}
    num_sys_set.update(n_numbers["otherNumberingSystems"].values())
    num_sys_set = num_sys_set & num_systems.keys()
    if len(num_sys_set) > 1:
        num_sys_set = num_sys_set - {"latn"}
    numbers = num_systems[num_sys_set.pop()]
    output["numbers"] = numbers[1:] + numbers[0]
    return output

def o3a(tag):
    t = Template(open("template.html").read())
    return t.render(**get_data(tag))

def generate_o3a(tag):
    open("output.html", "w").write(o3a(tag))
