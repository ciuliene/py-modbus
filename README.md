# py-modbus

[![codecov](https://codecov.io/gh/ciuliene/py-modbus/graph/badge.svg?token=C11TGTYP5F)](https://codecov.io/gh/ciuliene/py-modbus)

Communicate with devices through serial using Modbus protocol.

## Installation

```sh
pip install -r requirements.txt
```

## Usage

```sh
usage: main.py [-h] [-m MESSAGE] [-f FILE] [-d DESTINATION] [-p PORT] [-b BAUDRATE] [-c] [-s] [-v]

Communicate with devices through serial using Modbus protocol.

options:
  -h, --help            show this help message and exit
  -m MESSAGE, --message MESSAGE
                        message to send
  -f FILE, --file FILE  path to file where to get messages to send (if '-m' is provided, this argument is ignored)
  -d DESTINATION, --destination DESTINATION
                        destination file for responses. Optional, if not provided the responses are printed on the console
  -p PORT, --port PORT  serial port
  -b BAUDRATE, --baudrate BAUDRATE
                        baudrate
  -c, --continuous      send messages continuously
  -s, --skip-crc        skip CRC
  -v, --verbose         print sent messages
```
