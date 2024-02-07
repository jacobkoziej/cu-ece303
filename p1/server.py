#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
#
# server.py -- simple HTTP server
# Copyright (C) 2024  Jacob Koziej <jacobkoziej@gmail.com>

import argparse
import socket


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
    sock.bind((args.address, args.port))
    sock.listen()

    sock.close()


if __name__ == '__main__':
    main()
