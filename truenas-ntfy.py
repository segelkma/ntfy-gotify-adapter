#!/usr/bin/env python3
import os
import sys
from aiohttp import web
from aiohttp import ClientSession

# The url the alerts should be forwarded to.
# Format: http[s]://{host}:{port}/channel
NTFY_BASEURL = os.environ.get("NTFY_URL")
# The token for the gotify application
# Example: cGVla2Fib29v
NTFY_TOKEN = os.environ.get("NTFY_TOKEN")

# The ip address the service should listen on
# Defaults to localhost for security reasons
LISTEN_HOST = os.environ.get("LISTEN_HOST", "127.0.0.1")
PORT = 31663


routes = web.RouteTableDef()

# Listen to post requests on / and /message
@routes.post("/")
@routes.post("/message")
async def on_message(request):
    content = await request.json()
    # The content of the alert message
    message = content["text"].strip().partition("\n")
    # Extract notification title from the message
    title = message[0].strip()
    message = message[2].strip()
    print(f"========== {title} ==========")
    print(message)
    print(f"{len(title) * '='}======================")

    # Forward the alert to ntfy
    ntfy_resp = await send_ntfy_message(message, NTFY_TOKEN, title=title)

    # Check for http reponse status code 'success'
    if ntfy_resp.status == 200:
        print(">> Forwarded successfully\n")
    elif ntfy_resp.status in [400, 401, 403]:
        print(f">> Unauthorized! Token NTFY_TOKEN='{NTFY_TOKEN}' is incorrect\n")
    else:
        print(f">> Unknown error while forwarding to ntfy. Error Code {ntfy_resp.status}")

    # Return the gotify status code to truenas
    return web.Response(status=ntfy_resp.status)

# Send an arbitrary alert to gotify
async def send_ntfy_message(message, token, title=None, priority=None):
    # Set token through header
    headers = {"Authorization": "Basic " + token}
    
    # Optional ntfy features
    if title:
        headers["Title"] = title
    if priority:
        headers["Priority"] = priority

    async with ClientSession() as session:
        async with session.post(NTFY_BASEURL, headers=headers, data=message.encode(encoding='utf-8')) as resp:
            return resp


if __name__ == "__main__":
    # Check if env variables are set
    if NTFY_BASEURL == None:
        sys.exit("Set ntfy Endpoint via 'NTFY_URL=http[s]://{host}:{port}/'!")
    if NTFY_TOKEN == None:
        sys.exit("Set ntfy App Token via 'NTFY_TOKEN={token}'!")

    # Listen
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host=LISTEN_HOST, port=PORT)
