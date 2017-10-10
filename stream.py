#!/usr/bin/env python
import argparse
import os
import subprocess
import sys

from utils import infile_type


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--left', required=True,
            type=lambda f: infile_type(parser, f),
            help='left channel input')
    parser.add_argument('-r', '--right', required=True,
            type=lambda f: infile_type(parser, f),
            help='right channel input')
    parser.add_argument('--audio', choices=['l', 'r'],
            help='audio source (left / right)')
    parser.add_argument('--host', default='127.0.0.1',
            help='address to bind to')
    parser.add_argument('-p', '--port', default=8100, type=int,
            help='port number to bind to')

    args = parser.parse_args()

    # Build FFmpeg command line
    cmd = [
        'ffmpeg',
        '-re',              # realtime - simulate camera feed
        '-i', args.left,
        '-i', args.right,
        '-c', 'copy',       # copy existing codec - assume already H.264/AAC
        '-f', 'rtp_mpegts',  # stream over RTP as an MPEG transport stream
        '-map', '0:v:0',    # left channel, first video stream
        '-map', '1:v:0',    # right channel, first video stream
    ]

    if args.audio == 'l':
        cmd.extend(['-map', '0:a:0'])
    elif args.audio == 'r':
        cmd.extend(['-map', '1:a:0'])

    cmd.append('rtp://{}:{}'.format(args.host, args.port))

    # Run FFmpeg
    return subprocess.call(cmd)


if __name__ == '__main__':
    sys.exit(main())
