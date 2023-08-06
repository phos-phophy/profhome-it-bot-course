## Description

The simplest tg bot that can register users (that's all)

## How to start

```
usage: main.py [-h] [-c CONFIG] [-t TOKEN]

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to the configuration file
  -t TOKEN, --token TOKEN
                        Bot HTTP API access token
```

### 1. First way:

1. Set `API_TOKEN` environment variable
   ```bash
   export API_TOKEN=YOUR_HTTP_API_TOKEN
   ```
2. Run in the command line `python3 main.py [-c CONFIG]`

### 2. Second way:

Run in the command line `python3 main.py -t YOUR_HTTP_API_TOKEN [-c CONFIG] `

## Commands

* `/help` - print help message
* `/start` - greet a unregistered user and offer to register
* `/change_name` - change username
