import argparse
from io import TextIOWrapper
from pyrocketmodbus import RocketModbus
from src.message import Message
import os
import time
import tempfile


def get_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Communicate with devices through serial using Modbus protocol.')
    parser.add_argument('-m', '--message', dest='message',
                        help='message to send')
    parser.add_argument('-f', '--file', dest='file',
                        help='path to file where to get messages to send (if \'-m\' is provided, this argument is ignored)')
    parser.add_argument('-d', '--destination', dest='destination',
                        help='destination file for responses. Optional, if not provided the responses are printed on the console')
    parser.add_argument('-p', '--port', dest='port', help='serial port')
    parser.add_argument('-b', '--baudrate', dest='baudrate', help='baudrate')
    parser.add_argument('-c', '--continuous', dest='continuous',
                        help='send messages continuously', action='store_true')
    parser.add_argument('-s', '--skip-crc', dest='skip_crc', help='skip CRC',
                        action='store_true')
    parser.add_argument('-v', '--verbose', dest='verbose',
                        help='print sent messages', action='store_true')
    parser.add_argument('-C', '--crc', dest='crc', help='Generate Modbus message with CRC and skip send', action='store_true')
    args = parser.parse_args()

    if not args.message and not args.file:
        parser.error('\033[31mYou must provide a message or a file\033[0m')

    if not args.message and args.file and not os.path.exists(args.file):
        abs_path_file = os.path.abspath(args.file)
        parser.error(
            f"\033[31mFile '\033[33m{abs_path_file}\033[31m' does not exist\033[0m")

    return args


def send_messages(rocket: RocketModbus, messages: list[list[str]], destination: TextIOWrapper | None = None, verbose: bool = False, skip_crc: bool = False) -> list[Message]:
    responses = []
    for message in messages:
        result, (send, recv) = rocket.send_message(message, skip_crc=skip_crc)

        if verbose:
            rocket.log_message(send, prefix='TX')

        responses.append(Message(send, recv))

        if result:
            rocket.log_message(recv, prefix='\tRX')
        else:
            print(f'Error: {recv}')  # pragma: no cover

        if destination:
            destination.write(f'{str(responses[-1])}\n')
    return responses


def parse_file(lines: list[str]) -> list[list[str]]:
    messages = []
    for line in lines:
        if line[0] == '#' or line[0] == '\n':
            continue
        m = line.split(' ')
        messages.append(m)
    return messages


def py_modbus(args: argparse.Namespace):
    try:
        if args.message:
            # Store message in a temporary file
            temp = tempfile.NamedTemporaryFile(mode='w', delete=False)
            temp.write(args.message)
            temp.close()
            args.file = temp.name
        
        rocket = RocketModbus()

        while True:
            with open(args.file, 'r') as file:
                content = file.readlines()
                messages = parse_file(content)

                if args.crc:
                    for message in messages:
                        msg = rocket.prepare_message(message)
                        rocket.log_message(msg, prefix='MSG')
                        pass
                    return

                destination = open(
                    args.destination, 'w') if args.destination else None

                if not rocket.open(port=args.port, baudrate=int(args.baudrate or 9600)):
                    raise Exception('Error opening serial port')
                send_messages(rocket, messages, destination, args.verbose, args.skip_crc)
                
                destination.close() if destination else None

            if not args.continuous:
                break
            else:
                time.sleep(0.05)

        return True
    except KeyboardInterrupt:
        print()
        return True
    except Exception as e:
        print(f'\033[31m{e}\033[0m')
        return False
    finally:
        close_port(rocket=rocket)

def close_port(rocket: RocketModbus):
    rocket.close()

if __name__ == '__main__':  # pragma: no cover
    args = get_arguments()
    py_modbus(args)
