#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
#
# server.py -- simple HTTP server
# Copyright (C) 2024  Jacob Koziej <jacobkoziej@gmail.com>

import argparse
import socket
import threading
import typing

from loguru import logger


BUFSIZE: typing.Final[int] = 4096
ENCODING: typing.Final[str] = 'utf-8'


def handle_client(conn: socket.socket, address: tuple[str, int]) -> None:
    try:
        request = conn.recv(BUFSIZE).decode(ENCODING)

        file = request.split()[1]
        file = file[1:]  # strip '/'

        logger.info(f'requested file: `{file}`')

        with open(file) as f:
            data = f.read()

        response = 'HTTP/1.0 200 OK\r\n\r\n' + data

    except IOError:
        logger.warning(f'`{file}` not found!')

        response = 'HTTP/1.0 404 NOT FOUND\r\n\r\n'

    finally:
        conn.sendall(response.encode(ENCODING))
        conn.close()


def main():
    parser = argparse.ArgumentParser(
        prog='server',
        description='simple HTTP server',
    )

    parser.add_argument(
        '-a',
        '--address',
        required=True,
        type=str,
    )
    parser.add_argument(
        '-p',
        '--port',
        required=True,
        type=int,
    )

    args = parser.parse_args()

    sock = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_STREAM,
    )
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((args.address, args.port))
    sock.listen()

    logger.info(f'bound socket on `{args.address}:{args.port}`')

    try:
        while True:
            conn, address = sock.accept()
            logger.info(
                f'got a new connection from `{address[0]}:{address[1]}`'
            )

            thread = threading.Thread(
                target=handle_client,
                args=(conn, address),
            )
            thread.start()
    except KeyboardInterrupt:
        pass

    finally:
        sock.close()

        logger.info('closed socket')


if __name__ == '__main__':
    main()
