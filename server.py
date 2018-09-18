#!/usr/bin/env python3
from o3a import o3a

from sanic import Sanic
from sanic.response import html

app = Sanic()
app.static("/static", "./static")

@app.route("/<tag>")
async def handler(request, tag):
    return html(o3a(tag))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
