#!/usr/bin/env python3
from o3a import o3a

from flask import Flask

app = Flask("o3a")

@app.route("/")
def default_handler():
    return o3a("en")

@app.route("/<tag>")
def tag_handler(tag="en"):
    try:
        return o3a(tag)
    except FileNotFoundError:
        return "NOPE"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
