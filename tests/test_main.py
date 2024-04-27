import unittest
from unittest.mock import MagicMock, patch, call
from main import *
from src.message import Message
from argparse import Namespace


@patch('sys.stderr')
@patch('sys.stdout')
class TestMain(unittest.TestCase):

    def get_arguments(self, message: str = None, file: str = None, destination: str = None, continuous: bool = False, verbose: bool = False):
        args = Namespace()
        args.message = message
        args.file = file
        args.destination = destination
        args.continuous = continuous
        args.verbose = verbose
        return args

    @patch('sys.exit')
    def test_getting_arguments_exit_when_message_nor_file_are_provided(self, mock_exit, *_):
        # Act
        result = get_arguments()

        # Assert
        self.assertIsNone(result.message)
        self.assertIn(call(2), mock_exit.mock_calls)

    @patch('os.path.exists', return_value=False)
    @patch('sys.argv', ['main.py', '-f', 'test.txt'])
    @patch('sys.exit')
    def test_getting_arguments_exit_when_file_does_not_exist(self, mock_exit, *_):
        # Act
        result = get_arguments()

        # Assert
        self.assertIsNone(result.message)
        self.assertIn(call(2), mock_exit.mock_calls)

    @patch.object(RocketModbus, 'open', return_value=False)
    def test_sending_message_raises_exception_when_port_is_not_open(self, *_):
        # Arrange
        args = self.get_arguments(
            message='0x01 0x03 0x00 0x00 0x00 0x01 0x84 0x0A')

        # Act
        with self.assertRaises(Exception):
            send_messages(args)

    @patch.object(RocketModbus, 'open', return_value=True)
    @patch.object(RocketModbus, 'log_message')
    @patch.object(RocketModbus, 'send_message')
    def test_sending_message_logs_sent_message(self, mock_send, mock_log, *_):
        # Arrange
        args = self.get_arguments(
            message='0x01 0x03 0x00 0x00 0x00 0x01 0x84 0x0A', verbose=True)
        mock_send.return_value = (
            True, (args.message.split(), args.message.split()))

        # Act
        send_messages(messages=[args.message.split()], verbose=True)

        # Assert
        self.assertIn(
            call(args.message.split(), prefix='TX'), mock_log.mock_calls)

    @patch.object(RocketModbus, 'open', return_value=True)
    @patch.object(RocketModbus, 'log_message')
    @patch.object(RocketModbus, 'send_message')
    def test_sending_message_save_communication_into_destination_file(self, mock_send, mock_log, *_):
        # Arrange
        args = self.get_arguments(
            message='0x01 0x03 0x00 0x00 0x00 0x01 0x84 0x0A', verbose=True)
        mock_send.return_value = (
            True, ([int(x, 16) for x in args.message.split()], [int(x, 16) for x in args.message.split()]))
        mock_destination = MagicMock()

        # Act
        send_messages(
            messages=[args.message.split()],
            destination=mock_destination)

        # Assert
        self.assertIn(call(f'{str(Message([int(x, 16) for x in args.message.split()], [int(
            x, 16) for x in args.message.split()]))}\n'), mock_destination.write.mock_calls)

    def test_parsing_file_skips_comments(self, *_):
        # Arrange
        lines = ['# Comment', '0x01 0x03 0x00 0x00 0x00 0x01 0x84 0x0A']

        # Act
        result = parse_file(lines)

        # Assert
        self.assertEqual(len(result), 1)

    def test_message_returns_expected_string(self, *_):
        # Arrange
        sent = [1, 3, 0, 0, 0, 1, 132, 10]
        received = [1, 3, 0, 0, 0, 1, 132, 10]

        # Act
        message = Message(sent, received)

        # Assert
        self.assertEqual(str(
            message), '0x01 - 0x03 - 0x00 - 0x00 - 0x00 - 0x01 - 0x84 - 0x0A    ->    0x01 - 0x03 - 0x00 - 0x00 - 0x00 - 0x01 - 0x84 - 0x0A')

    def test_py_modbus_returns_true_when_message_is_sent_correctly(self, *_):
        # Arrange
        args = self.get_arguments(
            message='0x01 0x03 0x00 0x00 0x00 0x01 0x84 0x0A')

        # Act
        result = py_modbus(args)

        # Assert
        self.assertTrue(result)

    @patch('builtins.open')
    def test_py_modbus_writes_into_destination_the_response(self, mock_open, *_):
        # Arrange
        args = self.get_arguments(
            message='0x01 0x03 0x00 0x00 0x00 0x01 0x84 0x0A', destination='test.txt')

        # Act
        py_modbus(args)

        # Assert
        self.assertIn(call('test.txt', 'w'), mock_open.mock_calls)

    @patch('time.sleep')
    def test_py_modbus_continuous_until_keyboard_interrupt(self, mock_sleep, *_):
        # Arrange
        args = self.get_arguments(
            message='0x01 0x03 0x00 0x00 0x00 0x01 0x84 0x0A', continuous=True)
        mock_sleep.side_effect = [None, None, KeyboardInterrupt]

        # Act
        result = py_modbus(args)

        # Assert
        mock_sleep.assert_called_with(0.05)
        self.assertTrue(result)

    @patch('builtins.open')
    def test_py_modbus_returns_false_when_exception_is_raised(self, mock_write, *_):
        # Arrange
        args = self.get_arguments(
            message='0x01 0x03 0x00 0x00 0x00 0x01 0x84 0x0A')
        mock_write.side_effect = Exception()

        # Act
        result = py_modbus(args)

        # Assert
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
