#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
#
# server.py -- simple HTTP server
# Copyright (C) 2024  Jacob Koziej <jacobkoziej@gmail.com>

import argparse
import socket
import typing

from loguru import logger


BUFSIZE: typing.Final[int] = 4096


def main():
    parser = argparse.ArgumentParser(
        prog='server',
        description='simple HTTP server',
    )

    parser.add_argument(
        "-a",
        "--address",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-p",
        "--port",
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

    while True:
        conn, address = sock.accept()
        logger.info(f'got a new connection from `{address[0]}:{address[1]}`')

        try:
            request = conn.recv(BUFSIZE).decode('utf-8')

            file = request.split()[1]
            file = file[1:]  # strip '/'

            logger.info(f'requested file: `{file}`')

        except IOError:
            logger.warning(f'`{file}` not found!')

    sock.close()


if __name__ == '__main__':
    main()
