#!/usr/bin/env python3
from o3a import o3a

from sanic import Sanic
from sanic.response import html

app = Sanic()
app.static("/static", "./static")

@app.route("/")
async def handler(request):
    return html(o3a("en"))

@app.route("/<tag>")
async def handler(request, tag="en"):
    try:
        return html(o3a(tag))
    except FileNotFoundError:
        return html("NOPE")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
