#!/usr/bin/env python
import argparse
import os
import subprocess
import sys

from utils import infile_type


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='3DS AVI file',
            type=lambda f: infile_type(parser, f))
    output_group = parser.add_argument_group('outputs')
    output_group.add_argument('-l', '--left',
            help='left channel filename')
    output_group.add_argument('-r', '--right',
            help='right channel filename')

    args = parser.parse_args()
    if (args.left is None) != (args.right is None):
        parser.error('-l/--left and -r/--right must be specified together')

    source = args.input
    if args.left is not None and args.right is not None:
        left, right = args.left, args.right
    else:
        base, ext = os.path.splitext(source)
        left = base + '_l.mjpg'
        right = base + '_r.mjpg'

    subprocess.call([
            'ffmpeg',
            '-i', source,
            '-c', 'copy',
            '-map', '0:v:0',
            left])
    subprocess.call([
            'ffmpeg',
            '-i', source,
            '-c', 'copy',
            '-map', '0:v:1',
            right])


if __name__ == '__main__':
    sys.exit(main())
