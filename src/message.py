class Message:
    def __init__(self, sent: list[int], received: list[int] | int) -> None:
        self.sent = sent
        self.received = received
        self.error = type(received) == int
        pass

    def __str__(self) -> str:

        sent = ' - '.join(
            ['0x' + '{:02x}'.format(byte).upper() for byte in self.sent])
        received = ' - '.join(
            ['0x' + '{:02x}'.format(byte).upper() for byte in self.received]) if not self.error else f'Error: {str(self.received)}'
        return f'{sent}    ->    {received}'
