FROM alpine:latest

RUN apk add --update --no-cache python3 py3-aiohttp

WORKDIR /app
COPY truenas-ntfy.py ./

CMD ["/usr/bin/env", "python3", "-u", "truenas-ntfy.py"]
