# Introduction

This is an client&server for sharing clipboard between different computers which running client.

Base on `Python3` and `WebSocket`.

Support on most platform running: `Windows`, `Linux`, `Macos`

# Requirements

Run command in Python3 enviroment at source root:

```
pip3 install -r requirements.txt
```

For linux system (`client only`), install external requirements:

```
pip3 install -r requirements.linux.txt
```

# Config

Config file is saved at `data/config.json`, run command to generate it:

```
python3 config.py
```

Server and client use the same config file, Config content:

```
{
    "server_setting": {
        "host": "0.0.0.0",
        "port": 10000
    }
}
```

Server:
1. `host`: bind address of web socket server
2. `port`: bind port of web socket server

Client:
1. `host`: server address which web socket serving
2. `port`: server port which web socket serving

# Run Server

```
python3 server.py
```

# Run Client

```
python3 client.py
```