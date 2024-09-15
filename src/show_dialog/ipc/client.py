import logging
import socket

from .ipc_params import IpcParams
from .message import Message


class IpcClient:
    def __init__(self, params: IpcParams):
        self.params = params

        # Create a socket object
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(self.params.timeout)

        # Connect to the server
        self.client_socket.connect((self.params.host, self.params.port))

    def send(self, message: Message):
        """Send a message ot the server."""
        try:
            message_json = message.to_json()
            logging.debug(f'Client sending: {message_json}')
            self.client_socket.sendall(message_json.encode())

            # Receive a response from the server
            response = self.client_socket.recv(self.params.buffer_size).decode()
            message_response = Message.from_json(response)
            logging.debug(f'Client received: {message_response.to_json()}')

        finally:
            # Close the connection
            self.client_socket.close()
            logging.debug('Client closed the connection.')
