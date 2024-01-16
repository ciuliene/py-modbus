# py-modbus

Send modbus commands to a device and get the responses.

## Installation

```sh
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple -r requirements.txt
```

## Usage

```sh
usage: main.py [-h] [-m MESSAGE] [-f FILE] [-d DESTINATION] [-c] [-v]

Send Modbus messages through serial.

options:
  -h, --help            show this help message and exit
  -m MESSAGE, --message MESSAGE
                        message to send
  -f FILE, --file FILE  path to file where to get messages to send (if '-m' is provided, this argument is ignored)
  -d DESTINATION, --destination DESTINATION
                        destination file for responses. Optional, if not provided the responses are printed on the console
  -c, --continuous      send messages continuously
  -v, --verbose         print sent messages
```
