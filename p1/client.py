#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
#
# client.py -- simple HTTP client
# Copyright (C) 2024  Jacob Koziej <jacobkoziej@gmail.com>

import argparse
import socket
import typing

from loguru import logger


BUFSIZE: typing.Final[int] = 4096
ENCODING: typing.Final[str] = 'utf-8'


def main():
    parser = argparse.ArgumentParser(
        prog='client',
        description='simple HTTP client',
    )

    parser.add_argument(
        '-a',
        '--address',
        required=True,
        type=str,
    )
    parser.add_argument(
        '-f',
        '--file',
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
    sock.connect((args.address, args.port))

    logger.info(f'connected socket to `{args.address}:{args.port}`')

    request = f'GET /{args.file} HTTP/1.1\r\n\r\n'
    sock.sendall(request.encode(ENCODING))

    response = sock.recv(BUFSIZE).decode(ENCODING)

    sock.close()

    logger.info('closed socket')

    print(response, end='')


if __name__ == '__main__':
    main()
