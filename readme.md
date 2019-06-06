# Introduction

This is a client&server for sharing clipboard between different computers which running client.

Base on `Python3` and `WebSocket`.

Support on most platform running: `Windows`, `Linux`, `Macos`

# Requirements

Run command in Python3 enviroment at source root:

```
pip3 install -r requirements.txt
```

For linux system (`client side`), install external requirements:

Ubuntu:

```
apt install xclip
```

Centos:

```
yum install xclip
```

Arch:

```
pacman -S xclip
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

# Build Client Bin

## Prepare

We can use `pyinstaller` to build. So, install `pyinstaller` to project python env.

```
pip3 install pyinstaller
```

## Windows

Make sure `rar` command first, add path of your `winrar` bin to system `PATH`.

Save following script to `build.windows.bat` at source root:

```
@echo off

echo ========================== make dist dir
rd /s /q dist
md "dist"
md "dist\extract"

echo ========================== copy config file
md "dist\data"
copy data\config.json dist\data

echo ========================== pack python code
rem Extract Dir(for debugging): --runtime-tmpdir extract

pyinstaller ^
--runtime-tmpdir extract ^
-F client.py

rem use in cmd line: for /f %i in ('git rev-parse --short HEAD') do set git_head=%i
rem use in bat script: for /f %%i in ('git rev-parse --short HEAD') do set git_head=%%i
for /f %%i in ('git rev-parse --short HEAD') do set git_head=%%i
echo %git_head%
set year=%date:~0,4%
set month=%date:~5,2%
set day=%date:~8,2%
cd dist
rar a -k -r -s -m1 clipboard.client.windows10.x64.%year%%month%%day%.%git_head%.rar .\
cd ..

start dist
echo script finished
pause
```

Run this script in project python environment `CMD`.

## Linux

Save following script to `build.linux.sh` at source root:

```
#!/usr/bin/env bash

echo ========================== make dist dir
rm -rf dist
mkdir dist
mkdir dist/extract

echo ========================== copy logger config file
mkdir dist/data
cp data/config.json dist/data/

echo ========================== pack python code
# Extract Dir(for debugging): --runtime-tmpdir extract

pyinstaller \
--runtime-tmpdir extract \
-F client.py

chmod 755 dist/client

cd dist
git_head=$(git rev-parse --short HEAD)
build_time=$(date "+%Y%m%d")
tar -cvf clipboard.client.linux.x64.$build_time.$git_head.tar *

cd ..
nautilus dist &

```

Run this script in project python environment `bash`.