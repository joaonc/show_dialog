import logging
import socket

from .ipc_params import IpcParams


class IpcClient:
    def __init__(self, params: IpcParams):
        self.params = params

        # Create a socket object
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(self.params.timeout)

        # Connect to the server
        self.client_socket.connect((self.params.host, self.params.port))

    def send(self, message: str):
        """Send a message ot the server."""
        try:
            logging.debug(f'Sending: {message}')
            self.client_socket.sendall(message.encode())

            # Receive a response from the server
            response = self.client_socket.recv(self.params.buffer_size).decode()
            logging.debug(f'Received from server: {response}')

        finally:
            # Close the connection
            self.client_socket.close()
            logging.debug('Client closed the connection.')
