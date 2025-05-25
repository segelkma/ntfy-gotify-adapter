# TrueNas ntfy Adapter

Adaptation of ZTubes TrueNas Gotify Adapter. TrueNas does not natively provide a way to send alerts and notifications to a ntfy server. This repo 'abuses' the TrueNas Slack alert integration and provides a fake slack webhook endpoint to forward alerts to a ntfy server. Current implementation only supports auth by token.
Note that Slack is not required at all for this integration to work.

## Installation
1. Apps -> Discover Apps -> Custom App
    - Enter an Application Name, e.g. "truenas-ntfy"
    - _Image Repository_: ghcr.io/segelkma/truenas-ntfy-adapter
    - _Image Tag_: main
    - Environment Variables:
        - _Name_: NTFY\_URL
        - _Value_: [your ntfy url including channel] e.g.https://ntfy.example.com/channelname
        - _Name_: NTFY\_TOKEN
        - _Value_: [your ntfy access token] e.g. tk_3uf2fb3u9

    - Network Configuration: 
        - Check _"Host Network"_
    - Save

OR

1. Apps -> Discover Apps -> Custom App -> Install via YAML
```yaml
services:
  ntfy-truenas-adapter:
    container_name: ntfy-truenas-adapter
    image: ghcr.io/segelkma/truenas-ntfy-adapter:main
    restart: unless-stopped
    environment:
      - NTFY_URL=<your ntfy url including channel> # e.g. https://ntfy.example.com/channelname
      - NTFY_TOKEN=<your ntfy access token> # e.g. tk_3uf2fb3u9
    network_mode: host
```

1. System -> Alert Settings -> Add
    - _Type_: Slack
    - _Webhook URL_: http://localhost:31663
    - Click _Send Test Alert_ to test the connection
    - Save
